#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((n) / POW10[i]) % 10)

#define ARRAY_SIZE(ar)  ((icsize_t)(sizeof(ar)/sizeof((ar)[0])))

static const int POW10[6] = { 1, 10, 100, 1000, 10000, 100000 };

typedef int64_t icword_t;
#define FMT_W  "%ld"
typedef int64_t icsize_t;
#define FMT_S  "%ld"

#define OP_ADD          1
#define OP_MUL          2
#define OP_INPUT        3
#define OP_OUTPUT       4
#define OP_JMP_TRUE     5
#define OP_JMP_FALSE    6
#define OP_LESS         7
#define OP_EQUAL        8
#define OP_BASE_ADD     9
#define OP_HLT          99

#define MODE_POSITION   0
#define MODE_IMMEDIATE  1
#define MODE_RELATIVE   2

#define OP(op)       ((op) % 100)
#define MODE(op, i)  DIGIT((op), (i) + 2)

#define MEM_SIZE_MAX  (64 * 1024)

typedef enum {
    ERR_SUCCESS     = 0,
    ERR_WAIT_INPUT  = 1,
    ERR_FAILURE     = -1,
} error_t;

#define ENABLE_DUMP   0
#define ENABLE_TRACE  0

#if ENABLE_TRACE
#define TRACE(msg)  do{ printf msg ; fflush(stdout); }while(0)
#else
#define TRACE(msg)
#endif


typedef struct software{
    icword_t *mem;
    icword_t size;
    error_t (*get_input)(struct software *, icword_t *);
    error_t (*set_output)(struct software *, icword_t);
    icsize_t pc;
    icsize_t base;
} software_t;

error_t soft_get_input_unimplemented(struct software *soft, icword_t *value)
{
    (void) soft;
    (void) value;
    PANIC("Unimplemented 'get_input' function");
    return ERR_FAILURE;
}

error_t soft_set_output_unimplemented(struct software *soft, icword_t value)
{
    (void) soft;
    (void) value;
    PANIC("Unimplemented 'set_input' function");
    return ERR_FAILURE;
}

static void software_init(software_t *soft)
{
    memset(soft, 0, sizeof(*soft));
    soft-> mem = malloc(MEM_SIZE_MAX);
    soft->get_input = soft_get_input_unimplemented;
    soft->set_output = soft_set_output_unimplemented;
}

static void software_destroy(software_t *soft)
{
    free(soft->mem);
}


typedef struct boost_soft {
    software_t soft;  // keep first
    icword_t output;
    int output_is_set;
} boost_soft_t;

#define SOFT_TO_BOOST(soft_ptr)  ((boost_soft_t *)(soft_ptr))
#define BOOST_TO_SOFT(boost_ptr)  (&((boost_ptr)->soft))

static error_t boost_get_input(software_t *soft, icword_t *value)
{
    boost_soft_t *boost = SOFT_TO_BOOST(soft);
    (void) boost;
    *value = 1;
    return ERR_SUCCESS;
}

static error_t boost_set_output(software_t *soft, icword_t value)
{
    boost_soft_t *boost = SOFT_TO_BOOST(soft);
    boost->output = value;
    if(boost->output_is_set) {
        printf("Detected incorrect opcode: "FMT_W"\n", value);
    } else {
        boost->output_is_set = 1;
    }
    return value;
}

static void boost_init(boost_soft_t *boost)
{
    software_t *soft = BOOST_TO_SOFT(boost);
    software_init(soft);
    soft->get_input = boost_get_input;
    soft->set_output = boost_set_output;
}

static void boost_destroy(boost_soft_t *boost)
{
    software_destroy(BOOST_TO_SOFT(boost));
}

static void dump(const icword_t *buf, icsize_t len)
{
#if ENABLE_DUMP
    // to redo
    (void) buf;
    (void) len;
#else
    (void) buf;
    (void) len;
#endif  /* ENABLE_DUMP */
}


static icword_t param_value(const software_t *soft, int idx)
{
    icword_t param = soft->mem[soft->pc+1+idx];
    int mode = MODE(soft->mem[soft->pc], idx);
    icword_t value;

    TRACE(("param "FMT_W", mode %d ", param, mode));

    switch(mode) {
        case MODE_POSITION:
            TRACE(("(read @"FMT_W")", param));
            value = soft->mem[param];
            break;
        case MODE_IMMEDIATE:
            value = param;
            break;
        case MODE_RELATIVE:
            TRACE(("(read @"FMT_S"+"FMT_W"="FMT_W")", soft->base, param, soft->base + param));
            value = soft->mem[soft->base + param];
            break;
        default:
            PANIC("Invalid mode");
    }
    TRACE((" -> "FMT_W"\n", value));
    return value;
}


static icsize_t param_pos(const software_t *soft, int idx)
{
    icword_t param = soft->mem[soft->pc+1+idx];
    int mode = MODE(soft->mem[soft->pc], idx);
    icsize_t pos;

    TRACE(("write_pos  "FMT_W", mode %d ", param, mode));

    switch(mode) {
        case MODE_POSITION:
            TRACE(("(write @"FMT_W")", param));
            pos = param;
            break;
        case MODE_IMMEDIATE:
            PANIC("lvalue cannot be in 'immediate' mode");
            break;
        case MODE_RELATIVE:
            pos = soft->base + param;
            TRACE(("(write @"FMT_S"+"FMT_W"="FMT_S")", soft->base, param, pos));
            break;
        default:
            PANIC("Invalid mode");
    }
    TRACE((" -> "FMT_S"\n", pos));
    return pos;
}


static int param_num(int op)
{
    switch(op) {
        case OP_ADD:       return 3;
        case OP_MUL:       return 3;
        case OP_INPUT:     return 1;
        case OP_OUTPUT:    return 1;
        case OP_JMP_TRUE:  return 2;
        case OP_JMP_FALSE: return 2;
        case OP_LESS:      return 3;
        case OP_EQUAL:     return 3;
        case OP_BASE_ADD:  return 1;
        case OP_HLT:       return 0;
        default:           PANIC("Unexpected op");
    }
}

static error_t run_program(software_t *soft)
{
    icword_t *mem = soft->mem;
    icsize_t size = soft->size;
    icword_t op;
    int pnum;
    icword_t param[8] = {0};
    icsize_t offset;
    int i;
    icword_t value;
    icsize_t write_pos;

    while(OP(mem[soft->pc]) != OP_HLT) {
        TRACE(("-----\n"));
        TRACE(("pc="FMT_S", ["FMT_W", "FMT_W", "FMT_W", "FMT_W"]\n",
            soft->pc, mem[soft->pc], mem[soft->pc+1], mem[soft->pc+2], mem[soft->pc+3]));

        dump(mem, soft->size);

        op = OP(mem[soft->pc]);
        pnum = param_num(op);
        for(i = 0; i < pnum; ++i) {
            param[i] = param_value(soft, i);
        }
        offset = pnum + 1;

        TRACE(("op="FMT_W", params: "FMT_W", "FMT_W"\n", op, param[0], param[1]));

        switch(op) {
            case OP_ADD:
                write_pos = param_pos(soft, 2);
                TRACE(("ADD: "FMT_W" + "FMT_W" -> ("FMT_S")\n", param[0], param[1], write_pos));
                mem[write_pos] = param[0] + param[1];
                break;

            case OP_MUL:
                write_pos = param_pos(soft, 2);
                TRACE(("MUL: "FMT_W" * "FMT_W" -> ("FMT_S")\n", param[0], param[1], write_pos));
                mem[write_pos] = param[0] * param[1];
                break;

            case OP_INPUT:
                switch(soft->get_input(soft, &value)) {
                    case ERR_SUCCESS:
                        write_pos = param_pos(soft, 0);
                        TRACE(("INPUT: "FMT_W" -> ("FMT_S")\n", value, write_pos));
                        mem[write_pos] = value;
                        break;
                    case ERR_WAIT_INPUT:
                        TRACE(("WAIT INPUT\n"));
                        return ERR_WAIT_INPUT;
                    case ERR_FAILURE:
                    default:
                        PANIC("Critical error");
                        break;
                }
                break;

            case OP_OUTPUT:
                TRACE(("OUTPUT: "FMT_W"\n", param[0]));
                soft->set_output(soft, param[0]);
                break;

            case OP_JMP_TRUE:
                TRACE(("JMPTRUE: "FMT_W"", param[0]));
                if(param[0]) {
                    TRACE((" -> true @"FMT_W"\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> false\n"));
                }
                break;

            case OP_JMP_FALSE:
                TRACE(("JMPTRUE: "FMT_W"", param[0]));
                if(!param[0]) {
                    TRACE((" -> false @"FMT_W"\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> true\n"));
                }
                break;

            case OP_LESS:
                write_pos = param_pos(soft, 2);
                TRACE(("LESS: "FMT_W" < "FMT_W" -> "FMT_S"\n", param[0], param[1], write_pos));
                mem[write_pos] = (param[0] < param[1]) ? 1 : 0;
                break;

            case OP_EQUAL:
                write_pos = param_pos(soft, 2);
                TRACE(("EQUAL: "FMT_W" == "FMT_W" -> "FMT_S"\n", param[0], param[1], write_pos));
                mem[write_pos] = (param[0] == param[1]) ? 1 : 0;
                break;

            case OP_BASE_ADD:
                TRACE(("BASE_ADD: "FMT_S" (+"FMT_W")", soft->base, param[0]));
                soft->base += param[0];
                TRACE((" -> "FMT_S"\n", soft->base));
                break;

            default:
                return ERR_FAILURE;
        }

        TRACE(("offset="FMT_S"\n", offset));
        soft->pc += offset;

        if(soft->pc > size) {
            return ERR_FAILURE;
        }
    }
    TRACE(("halt\n"));
    dump(mem, size);

    return ERR_SUCCESS;
}


/* Return number of positions, or -1 for failure. */
static int read_software(software_t *soft, const char *filename)
{
    FILE *f;
    icsize_t pos_num = 0;
    icword_t value;
    int n;

    f = fopen(filename, "rb");
    if(!f) {
        PANIC("Could not read file");
    }

    while(1) {
        if(pos_num > (MEM_SIZE_MAX / (int) sizeof(icword_t))) {
            PANIC("Too many positions");
        }

        n = fscanf(f, FMT_W",", &value);
        if(n < 1) {
            break;
        }
        soft->mem[soft->size++] = value;
    }

    fclose(f);
    return ERR_SUCCESS;
}


int main(int argc, char **argv)
{
    boost_soft_t boost = {0};
    boost_init(&boost);

    if(argc >= 2) {
        if(read_software(BOOST_TO_SOFT(&boost), argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    if(run_program(BOOST_TO_SOFT(&boost)) != ERR_SUCCESS) {
        PANIC("Something went wrong");
    }
    if(!boost.output_is_set) {
        PANIC("BOOST did not produce any output");
    }

    printf("Result: "FMT_W"\n", boost.output);

    boost_destroy(&boost);

    return 0;
}
