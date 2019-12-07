#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((n) / POW10[i]) % 10)

#define ARRAY_SIZE(ar)  ((int)(sizeof(ar)/sizeof((ar)[0])))

static const int POW10[6] = { 1, 10, 100, 1000, 10000, 100000 };
static const int PHASE_SETTINGS[120][5];  // see bottom

#define OP_ADD       1
#define OP_MUL       2
#define OP_INPUT     3
#define OP_OUTPUT    4
#define OP_JMP_TRUE  5
#define OP_JMP_FALSE 6
#define OP_LESS      7
#define OP_EQUAL     8
#define OP_HLT       99

#define MODE_POSITION   0
#define MODE_IMMEDIATE  1

#define OP(op)       ((op) % 100)
#define MODE(op, i)  DIGIT((op), (i) + 2)

#define MEM_SIZE_MAX  (16 * 1024)
#define AMP_NUM       5

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
    int mem[MEM_SIZE_MAX];
    int size;
    error_t (*get_input)(struct software *, int *);
    error_t (*set_output)(struct software *, int);
    int pc;
} software_t;


typedef struct amp_soft {
    software_t soft;
    int phase;
    int is_configured;
    int input_valid;
    int input;
    struct amp_soft *output;
} amp_soft_t;

#define SOFT_TO_AMP(soft_ptr)  ((amp_soft_t *)(soft_ptr))
#define AMP_TO_SOFT(amp_ptr)  ((software_t *)(amp_ptr))


static void dump(const int *buf, int len)
{
#if ENABLE_DUMP
    int i, width = 0;

    printf("> ");
    for(i = 0; i < len; ++i) {
        printf("%d, ", buf[i]);
        width++;
        if((buf[i] == OP_HLT) || (width >= 4)) {
            printf("\n  ");
            width = 0;
        }
    }
    printf("\n");
#else
    (void) buf;
    (void) len;
#endif  /* ENABLE_DUMP */
}

static int param_value(const int *buf, int param, int mode)
{
    int value;

    TRACE(("param %d, mode %d", param, mode));

    switch(mode) {
        case MODE_POSITION:  value = buf[param]; break;
        case MODE_IMMEDIATE: value = param;      break;
        default: PANIC("Invalid mode");
    }
    TRACE((" -> %d\n", value));
    return value;
}


static error_t run_program(software_t *soft)
{
    int *mem = soft->mem;
    int size = soft->size;
    int op;
    int param[2] = {0};
    int offset;
    int i;
    int value;

    while(OP(mem[soft->pc]) != OP_HLT) {
        TRACE(("-----\n"));
        TRACE(("pc=%d, [%d, %d, %d, %d]\n",
            soft->pc, mem[soft->pc], mem[soft->pc+1], mem[soft->pc+2], mem[soft->pc+3]));

        dump(mem, soft->size);

        op = OP(mem[soft->pc]);
        for(i = 0; i < (int) (sizeof(param)/sizeof(int)); ++i) {
            param[i] = param_value(mem, mem[soft->pc+i+1], MODE(mem[soft->pc], i));
        }

        TRACE(("op=%d, params: %d, %d\n", op, param[0], param[1]));

        switch(op) {
            case OP_ADD:
                TRACE(("ADD: %d + %d -> (%d)\n", param[0], param[1], mem[soft->pc+3]));
                mem[mem[soft->pc+3]] = param[0] + param[1];
                offset = 4;
                break;

            case OP_MUL:
                TRACE(("MUL: %d * %d -> (%d)\n", param[0], param[1], mem[soft->pc+3]));
                mem[mem[soft->pc+3]] = param[0] * param[1];
                offset = 4;
                break;

            case OP_INPUT:
                switch(soft->get_input(soft, &value)) {
                    case ERR_SUCCESS:
                        TRACE(("INPUT: %d -> (%d)\n", value, mem[soft->pc+1]));
                        mem[mem[soft->pc+1]] = value;
                        offset = 2;
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
                TRACE(("OUTPUT: %d\n", param[0]));
                soft->set_output(soft, param[0]);
                offset = 2;
                break;

            case OP_JMP_TRUE:
                TRACE(("JMPTRUE: %d", param[0]));
                if(param[0]) {
                    TRACE((" -> true @%d\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> false\n"));
                    offset = 3;
                }
                break;

            case OP_JMP_FALSE:
                TRACE(("JMPTRUE: %d", param[0]));
                if(!param[0]) {
                    TRACE((" -> false @%d\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> true\n"));
                    offset = 3;
                }
                break;

            case OP_LESS:
                TRACE(("LESS: %d < %d -> %d\n", param[0], param[1], mem[soft->pc+3]));
                mem[mem[soft->pc+3]] = (param[0] < param[1]) ? 1 : 0;
                offset = 4;
                break;

            case OP_EQUAL:
                TRACE(("EQUAL: %d == %d -> %d\n", param[0], param[1], mem[soft->pc+3]));
                mem[mem[soft->pc+3]] = (param[0] == param[1]) ? 1 : 0;
                offset = 4;
                break;


            default:
                return ERR_FAILURE;
        }

        TRACE(("offset=%d\n", offset));

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
static int read_input(const char *filename, int *buf, int len)
{
    FILE *f;
    int pos_num = 0;
    int value;
    int n;

    f = fopen(filename, "rb");
    if(!f) {
        PANIC("Could not read file");
    }

    while(1) {
        if(pos_num > len) {
            PANIC("Too many positions");
        }

        n = fscanf(f, "%d,", &value);
        if(n < 1) {
            break;
        }
        buf[pos_num++] = value;
    }

    fclose(f);
    return pos_num;
}


error_t amp_get_input(software_t *soft, int *value)
{
    amp_soft_t *amp = SOFT_TO_AMP(soft);

    if(!amp->is_configured) {
        *value = amp->phase;
        amp->is_configured = 1;
        return ERR_SUCCESS;
    } else if(amp->input_valid) {
        *value = amp->input;
        amp->input_valid = 0;
        return ERR_SUCCESS;
    } else {
        return ERR_WAIT_INPUT;
    }
}


error_t amp_set_output(software_t *soft, int value)
{
    amp_soft_t *out_amp = SOFT_TO_AMP(soft)->output;
    out_amp->input = value;
    out_amp->input_valid = 1;
    return value;
}


int find_highest(const software_t *soft) {
    int setting;
    int amp;
    int out_value;
    int max_signal = 0;
    amp_soft_t amps[AMP_NUM] = {0};
    unsigned halted;  // bitfield
    const unsigned ALL_HALTED = ((1U << AMP_NUM) -1);

    for(setting = 0; setting < (int) ARRAY_SIZE(PHASE_SETTINGS); ++setting) {
        for(amp = 0; amp < ARRAY_SIZE(amps); ++amp) {
            memcpy(&amps[amp].soft, soft, sizeof(amps[0]));
            amps[amp].phase = PHASE_SETTINGS[setting][amp];
            amps[amp].is_configured = 0;
            amps[amp].input_valid = (amp == 0);
            amps[amp].input = 0;
            amps[amp].output = &amps[(amp+1)%ARRAY_SIZE(amps)];
        }

        halted = 0;
        while(halted != ALL_HALTED) {
            for(amp = 0; amp < AMP_NUM; ++amp) {
                switch(run_program(AMP_TO_SOFT(&amps[amp]))) {
                    case ERR_SUCCESS:
                        halted |= (1U << amp);
                        break;
                    case ERR_WAIT_INPUT:
                        break;
                    case ERR_FAILURE:
                        PANIC("Something wrong happened");
                        break;
                }
            }
            TRACE(("halted: %x\n", halted));
        }

        out_value = amps[AMP_NUM-1].output->input;
        if(out_value > max_signal) {
            max_signal = out_value;
        }
    }

    return max_signal;
}


int main(int argc, char **argv)
{
    software_t soft = {0};

    if(argc >= 2) {
        soft.size = read_input(argv[1], soft.mem, sizeof(soft.mem));
        if(soft.size < 0) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    soft.get_input = amp_get_input;
    soft.set_output = amp_set_output;
    printf("Result: %d\n", find_highest(&soft));

    return 0;
}

static const int PHASE_SETTINGS[120][5] = {
    { 5, 6, 7, 8, 9 },
    { 5, 6, 7, 9, 8 },
    { 5, 6, 8, 7, 9 },
    { 5, 6, 8, 9, 7 },
    { 5, 6, 9, 7, 8 },
    { 5, 6, 9, 8, 7 },
    { 5, 7, 6, 8, 9 },
    { 5, 7, 6, 9, 8 },
    { 5, 7, 8, 6, 9 },
    { 5, 7, 8, 9, 6 },
    { 5, 7, 9, 6, 8 },
    { 5, 7, 9, 8, 6 },
    { 5, 8, 6, 7, 9 },
    { 5, 8, 6, 9, 7 },
    { 5, 8, 7, 6, 9 },
    { 5, 8, 7, 9, 6 },
    { 5, 8, 9, 6, 7 },
    { 5, 8, 9, 7, 6 },
    { 5, 9, 6, 7, 8 },
    { 5, 9, 6, 8, 7 },
    { 5, 9, 7, 6, 8 },
    { 5, 9, 7, 8, 6 },
    { 5, 9, 8, 6, 7 },
    { 5, 9, 8, 7, 6 },
    { 6, 5, 7, 8, 9 },
    { 6, 5, 7, 9, 8 },
    { 6, 5, 8, 7, 9 },
    { 6, 5, 8, 9, 7 },
    { 6, 5, 9, 7, 8 },
    { 6, 5, 9, 8, 7 },
    { 6, 7, 5, 8, 9 },
    { 6, 7, 5, 9, 8 },
    { 6, 7, 8, 5, 9 },
    { 6, 7, 8, 9, 5 },
    { 6, 7, 9, 5, 8 },
    { 6, 7, 9, 8, 5 },
    { 6, 8, 5, 7, 9 },
    { 6, 8, 5, 9, 7 },
    { 6, 8, 7, 5, 9 },
    { 6, 8, 7, 9, 5 },
    { 6, 8, 9, 5, 7 },
    { 6, 8, 9, 7, 5 },
    { 6, 9, 5, 7, 8 },
    { 6, 9, 5, 8, 7 },
    { 6, 9, 7, 5, 8 },
    { 6, 9, 7, 8, 5 },
    { 6, 9, 8, 5, 7 },
    { 6, 9, 8, 7, 5 },
    { 7, 5, 6, 8, 9 },
    { 7, 5, 6, 9, 8 },
    { 7, 5, 8, 6, 9 },
    { 7, 5, 8, 9, 6 },
    { 7, 5, 9, 6, 8 },
    { 7, 5, 9, 8, 6 },
    { 7, 6, 5, 8, 9 },
    { 7, 6, 5, 9, 8 },
    { 7, 6, 8, 5, 9 },
    { 7, 6, 8, 9, 5 },
    { 7, 6, 9, 5, 8 },
    { 7, 6, 9, 8, 5 },
    { 7, 8, 5, 6, 9 },
    { 7, 8, 5, 9, 6 },
    { 7, 8, 6, 5, 9 },
    { 7, 8, 6, 9, 5 },
    { 7, 8, 9, 5, 6 },
    { 7, 8, 9, 6, 5 },
    { 7, 9, 5, 6, 8 },
    { 7, 9, 5, 8, 6 },
    { 7, 9, 6, 5, 8 },
    { 7, 9, 6, 8, 5 },
    { 7, 9, 8, 5, 6 },
    { 7, 9, 8, 6, 5 },
    { 8, 5, 6, 7, 9 },
    { 8, 5, 6, 9, 7 },
    { 8, 5, 7, 6, 9 },
    { 8, 5, 7, 9, 6 },
    { 8, 5, 9, 6, 7 },
    { 8, 5, 9, 7, 6 },
    { 8, 6, 5, 7, 9 },
    { 8, 6, 5, 9, 7 },
    { 8, 6, 7, 5, 9 },
    { 8, 6, 7, 9, 5 },
    { 8, 6, 9, 5, 7 },
    { 8, 6, 9, 7, 5 },
    { 8, 7, 5, 6, 9 },
    { 8, 7, 5, 9, 6 },
    { 8, 7, 6, 5, 9 },
    { 8, 7, 6, 9, 5 },
    { 8, 7, 9, 5, 6 },
    { 8, 7, 9, 6, 5 },
    { 8, 9, 5, 6, 7 },
    { 8, 9, 5, 7, 6 },
    { 8, 9, 6, 5, 7 },
    { 8, 9, 6, 7, 5 },
    { 8, 9, 7, 5, 6 },
    { 8, 9, 7, 6, 5 },
    { 9, 5, 6, 7, 8 },
    { 9, 5, 6, 8, 7 },
    { 9, 5, 7, 6, 8 },
    { 9, 5, 7, 8, 6 },
    { 9, 5, 8, 6, 7 },
    { 9, 5, 8, 7, 6 },
    { 9, 6, 5, 7, 8 },
    { 9, 6, 5, 8, 7 },
    { 9, 6, 7, 5, 8 },
    { 9, 6, 7, 8, 5 },
    { 9, 6, 8, 5, 7 },
    { 9, 6, 8, 7, 5 },
    { 9, 7, 5, 6, 8 },
    { 9, 7, 5, 8, 6 },
    { 9, 7, 6, 5, 8 },
    { 9, 7, 6, 8, 5 },
    { 9, 7, 8, 5, 6 },
    { 9, 7, 8, 6, 5 },
    { 9, 8, 5, 6, 7 },
    { 9, 8, 5, 7, 6 },
    { 9, 8, 6, 5, 7 },
    { 9, 8, 6, 7, 5 },
    { 9, 8, 7, 5, 6 },
    { 9, 8, 7, 6, 5 },
};
