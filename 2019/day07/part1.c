#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((n) / POW10[i]) % 10)

#define ARRAY_SIZE(ar)  (sizeof(ar)/sizeof((ar)[0]))

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

#define NOUN  1
#define VERB  2
#define INPUT_RANGE  100

#define ENABLE_DUMP   0
#define ENABLE_TRACE  0

#if ENABLE_TRACE
#define TRACE(msg)  do{ printf msg ; fflush(stdout); }while(0)
#else
#define TRACE(msg)
#endif


//static int buf[MEM_SIZE_MAX] = {0};
//int pos_num;

typedef struct {
    int mem[MEM_SIZE_MAX];
    int size;
} software_t;


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

static int inputs[64] = {0};
static int inputs_idx = 0;

static int get_input(void) {
    int value = inputs[inputs_idx++];
    TRACE(("get_input, idx %d -> %d\n", inputs_idx-1, value));
    return value;
}

static int err_value = 0;

static int set_output(int value) {
    TRACE(("set_output -> %d\n", err_value));
    err_value = value;
    return value;
}


/* Return 0 for success, non-nul value for failure */
static int run_program(software_t *soft)
{
    int *mem = soft->mem;
    int size = soft->size;
    int pc = 0;
    int op;
    int param[2] = {0};
    int offset;
    int i;
    int value;

    while(OP(mem[pc]) != OP_HLT) {
        TRACE(("-----\n"));
        TRACE(("pc=%d, [%d, %d, %d, %d]\n",
            pc, mem[pc], mem[pc+1], mem[pc+2], mem[pc+3]));

        dump(mem, soft->size);

        op = OP(mem[pc]);
        for(i = 0; i < (int) (sizeof(param)/sizeof(int)); ++i) {
            param[i] = param_value(mem, mem[pc+i+1], MODE(mem[pc], i));
        }

        TRACE(("op=%d, params: %d, %d\n", op, param[0], param[1]));

        switch(op) {
            case OP_ADD:
                TRACE(("ADD: %d + %d -> (%d)\n", param[0], param[1], mem[pc+3]));
                mem[mem[pc+3]] = param[0] + param[1];
                offset = 4;
                break;

            case OP_MUL:
                TRACE(("MUL: %d * %d -> (%d)\n", param[0], param[1], mem[pc+3]));
                mem[mem[pc+3]] = param[0] * param[1];
                offset = 4;
                break;

            case OP_INPUT:
                value = get_input();
                TRACE(("INPUT: %d -> (%d)\n", value, mem[pc+1]));
                mem[mem[pc+1]] = value;
                offset = 2;
                break;

            case OP_OUTPUT:
                TRACE(("OUTPUT: %d\n", param[0]));
                set_output(param[0]);
                offset = 2;
                break;

            case OP_JMP_TRUE:
                TRACE(("JMPTRUE: %d", param[0]));
                if(param[0]) {
                    TRACE((" -> true @%d\n", param[1]));
                    pc = param[1];
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
                    pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> true\n"));
                    offset = 3;
                }
                break;

            case OP_LESS:
                TRACE(("LESS: %d < %d -> %d\n", param[0], param[1], mem[pc+3]));
                mem[mem[pc+3]] = (param[0] < param[1]) ? 1 : 0;
                offset = 4;
                break;

            case OP_EQUAL:
                TRACE(("EQUAL: %d == %d -> %d\n", param[0], param[1], mem[pc+3]));
                mem[mem[pc+3]] = (param[0] == param[1]) ? 1 : 0;
                offset = 4;
                break;


            default:
                return 1;
        }

        TRACE(("offset=%d\n", offset));

        pc += offset;

        if(pc > size) {
            return 1;
        }
    }
    TRACE(("halt\n"));
    dump(mem, size);

    return 0;
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


int find_highest(const software_t *soft) {
    int setting;
    int amp;
    int max_signal = 0;
    software_t softrun;

    for(setting = 0; setting < (int) ARRAY_SIZE(PHASE_SETTINGS); ++setting) {

        err_value = 0;

        for(amp = 0; amp < 5; ++amp) {

            //printf("=====\nsetting %d, amp %d, err_value %d\n", setting, amp, err_value);
            inputs[0] = PHASE_SETTINGS[setting][amp];
            inputs[1] = err_value;
            inputs_idx = 0;
            memcpy(&softrun, soft, sizeof(softrun));

            if(run_program(&softrun)) {
                PANIC("Something wrong happened");
            }
        }

        if(err_value > max_signal) {
            max_signal = err_value;
            //printf("max_signal -> %d\n", max_signal);
        }
    }

    return max_signal;
}


int main(int argc, char **argv)
{
    software_t soft_input = {0};

    if(argc >= 2) {
        soft_input.size = read_input(argv[1], soft_input.mem, sizeof(soft_input.mem));
        if(soft_input.size < 0) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }


    printf("Result: %d\n", find_highest(&soft_input));

    return 0;
}

static const int PHASE_SETTINGS[120][5] = {
    { 0, 1, 2, 3, 4 },
    { 0, 1, 2, 4, 3 },
    { 0, 1, 3, 2, 4 },
    { 0, 1, 3, 4, 2 },
    { 0, 1, 4, 2, 3 },
    { 0, 1, 4, 3, 2 },
    { 0, 2, 1, 3, 4 },
    { 0, 2, 1, 4, 3 },
    { 0, 2, 3, 1, 4 },
    { 0, 2, 3, 4, 1 },
    { 0, 2, 4, 1, 3 },
    { 0, 2, 4, 3, 1 },
    { 0, 3, 1, 2, 4 },
    { 0, 3, 1, 4, 2 },
    { 0, 3, 2, 1, 4 },
    { 0, 3, 2, 4, 1 },
    { 0, 3, 4, 1, 2 },
    { 0, 3, 4, 2, 1 },
    { 0, 4, 1, 2, 3 },
    { 0, 4, 1, 3, 2 },
    { 0, 4, 2, 1, 3 },
    { 0, 4, 2, 3, 1 },
    { 0, 4, 3, 1, 2 },
    { 0, 4, 3, 2, 1 },
    { 1, 0, 2, 3, 4 },
    { 1, 0, 2, 4, 3 },
    { 1, 0, 3, 2, 4 },
    { 1, 0, 3, 4, 2 },
    { 1, 0, 4, 2, 3 },
    { 1, 0, 4, 3, 2 },
    { 1, 2, 0, 3, 4 },
    { 1, 2, 0, 4, 3 },
    { 1, 2, 3, 0, 4 },
    { 1, 2, 3, 4, 0 },
    { 1, 2, 4, 0, 3 },
    { 1, 2, 4, 3, 0 },
    { 1, 3, 0, 2, 4 },
    { 1, 3, 0, 4, 2 },
    { 1, 3, 2, 0, 4 },
    { 1, 3, 2, 4, 0 },
    { 1, 3, 4, 0, 2 },
    { 1, 3, 4, 2, 0 },
    { 1, 4, 0, 2, 3 },
    { 1, 4, 0, 3, 2 },
    { 1, 4, 2, 0, 3 },
    { 1, 4, 2, 3, 0 },
    { 1, 4, 3, 0, 2 },
    { 1, 4, 3, 2, 0 },
    { 2, 0, 1, 3, 4 },
    { 2, 0, 1, 4, 3 },
    { 2, 0, 3, 1, 4 },
    { 2, 0, 3, 4, 1 },
    { 2, 0, 4, 1, 3 },
    { 2, 0, 4, 3, 1 },
    { 2, 1, 0, 3, 4 },
    { 2, 1, 0, 4, 3 },
    { 2, 1, 3, 0, 4 },
    { 2, 1, 3, 4, 0 },
    { 2, 1, 4, 0, 3 },
    { 2, 1, 4, 3, 0 },
    { 2, 3, 0, 1, 4 },
    { 2, 3, 0, 4, 1 },
    { 2, 3, 1, 0, 4 },
    { 2, 3, 1, 4, 0 },
    { 2, 3, 4, 0, 1 },
    { 2, 3, 4, 1, 0 },
    { 2, 4, 0, 1, 3 },
    { 2, 4, 0, 3, 1 },
    { 2, 4, 1, 0, 3 },
    { 2, 4, 1, 3, 0 },
    { 2, 4, 3, 0, 1 },
    { 2, 4, 3, 1, 0 },
    { 3, 0, 1, 2, 4 },
    { 3, 0, 1, 4, 2 },
    { 3, 0, 2, 1, 4 },
    { 3, 0, 2, 4, 1 },
    { 3, 0, 4, 1, 2 },
    { 3, 0, 4, 2, 1 },
    { 3, 1, 0, 2, 4 },
    { 3, 1, 0, 4, 2 },
    { 3, 1, 2, 0, 4 },
    { 3, 1, 2, 4, 0 },
    { 3, 1, 4, 0, 2 },
    { 3, 1, 4, 2, 0 },
    { 3, 2, 0, 1, 4 },
    { 3, 2, 0, 4, 1 },
    { 3, 2, 1, 0, 4 },
    { 3, 2, 1, 4, 0 },
    { 3, 2, 4, 0, 1 },
    { 3, 2, 4, 1, 0 },
    { 3, 4, 0, 1, 2 },
    { 3, 4, 0, 2, 1 },
    { 3, 4, 1, 0, 2 },
    { 3, 4, 1, 2, 0 },
    { 3, 4, 2, 0, 1 },
    { 3, 4, 2, 1, 0 },
    { 4, 0, 1, 2, 3 },
    { 4, 0, 1, 3, 2 },
    { 4, 0, 2, 1, 3 },
    { 4, 0, 2, 3, 1 },
    { 4, 0, 3, 1, 2 },
    { 4, 0, 3, 2, 1 },
    { 4, 1, 0, 2, 3 },
    { 4, 1, 0, 3, 2 },
    { 4, 1, 2, 0, 3 },
    { 4, 1, 2, 3, 0 },
    { 4, 1, 3, 0, 2 },
    { 4, 1, 3, 2, 0 },
    { 4, 2, 0, 1, 3 },
    { 4, 2, 0, 3, 1 },
    { 4, 2, 1, 0, 3 },
    { 4, 2, 1, 3, 0 },
    { 4, 2, 3, 0, 1 },
    { 4, 2, 3, 1, 0 },
    { 4, 3, 0, 1, 2 },
    { 4, 3, 0, 2, 1 },
    { 4, 3, 1, 0, 2 },
    { 4, 3, 1, 2, 0 },
    { 4, 3, 2, 0, 1 },
    { 4, 3, 2, 1, 0 },
};
