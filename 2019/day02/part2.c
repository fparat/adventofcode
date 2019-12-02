#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg); exit(1); }while(0)

#define OP_ADD  1
#define OP_MUL  2
#define OP_HLT  99

#define MEM_SIZE_MAX  256

#define NOUN  1
#define VERB  2
#define INPUT_RANGE  100

#define ENABLE_DUMP  0

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
#endif  /* ENABLE_DUMP */
}


/* Return 0 for success, non-nul value for failure */
static int run_program(int *buf, int len)
{
    int pc = 0;

    while(buf[pc] != OP_HLT) {
        dump(buf, len);
        switch(buf[pc]) {
            case OP_ADD:
                buf[buf[pc + 3]] = buf[buf[pc + 1]] + buf[buf[pc + 2]];
                break;

            case OP_MUL:
                buf[buf[pc + 3]] = buf[buf[pc + 1]] * buf[buf[pc + 2]];
                break;

            default:
                return 1;
        }

        pc += 4;

        if(pc > len) {
            return 1;
        }
    }
    dump(buf,len);

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


static int find_pair(const int *buf, int len, int target)
{
    int mem[MEM_SIZE_MAX] = {0};
    int noun, verb;

    for(noun = 0; noun < INPUT_RANGE; ++noun) {
        for(verb = 0; verb < INPUT_RANGE; ++verb) {
            memcpy(mem, buf, len * sizeof(int));

            mem[NOUN] = noun;
            mem[VERB] = verb;

            if(run_program(mem, len)) {
                PANIC("Something went wrong");
            }

            if(mem[0] == target) {
                return 100 * noun + verb;
            }
        }
    }

    return -1;
}

int main(int argc, char **argv)
{
    int buf[MEM_SIZE_MAX] = {0};
    int pos_num;
    int target;

    if(argc >= 2) {
        pos_num = read_input(argv[1], buf, sizeof(buf));
        if(pos_num < 0) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    if(argc >= 3) {
        target = atoi(argv[2]);
    } else {
        PANIC("Please give target in argument 2");
    }

    printf("Result: %d\n", find_pair(buf, pos_num, target));

    return 0;
}
