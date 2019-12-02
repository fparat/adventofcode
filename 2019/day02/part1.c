#include <stdlib.h>
#include <stdio.h>

#define PANIC(msg)  do{ printf(msg); exit(1); }while(0)

#define OP_ADD  1
#define OP_MUL  2
#define OP_HLT  99


static void dump(const int *buf, int len)
{
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


int main(int argc, char **argv)
{
    int buf[4096] = {0};
    int pos_num;

    if(argc < 2) {
        PANIC("Please give input file in argument");
    }

    pos_num = read_input(argv[1], buf, sizeof(buf));
    if(pos_num < 0) {
        PANIC("Error reading input");
    }

    buf[1] = 12;
    buf[2] = 2;

    if(run_program(buf, pos_num)) {
        PANIC("Something went wrong");
    }

    printf("Result: %d\n", buf[0]);

    return 0;
}
