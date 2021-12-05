#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "intcode.h"

#define MAX_ROWS 128
#define MAX_COLS 128


typedef struct {
    software_t soft;
    char output;
    char **cells;
} droid_t;

#define TO_DROID(soft_ptr) ((droid_t *) (soft_ptr))

static error_t droid_set_output(software_t *soft, icword_t value)
{
    droid_t *droid = TO_DROID(soft);
    droid->output = (char) value;
    return ERR_YIELD_OUTPUT;
}

static droid_t *droid_new(void)
{
    droid_t *droid = malloc(sizeof(droid_t));
    memset(droid, 0, sizeof(*droid));
    intcode_init(&droid->soft);
    droid->soft.set_output = droid_set_output;
    droid->cells = calloc(MAX_ROWS, sizeof(char *));
    for(int y = 0; y < MAX_ROWS; ++y) {
        droid->cells[y] = calloc(MAX_COLS, 1);
    }

    return droid;
}

static void droid_delete(droid_t *droid)
{
    intcode_destroy(&droid->soft);
    for(int y = 0; y < MAX_ROWS; ++y) {
        free(droid->cells[y]);
    }
    free(droid->cells);
    free(droid);
}

static void droid_run(droid_t *droid)
{
    error_t err;
    int x = 0, y = 0;

    while((err = intcode_run(&droid->soft)) != ERR_SUCCESS) {
        if(err != ERR_YIELD_OUTPUT) {
            PANIC("intcode error");
        }

        char c = droid->output;

        droid->cells[y][x] = c;

        if(c == '\n') {
            x = 0;
            y += 1;
        } else {
            x += 1;
        }

        if(x >= MAX_COLS) {
            PANIC("not enough columns");
        } else if(y >= MAX_ROWS) {
            PANIC("not enough rows");
        }

        printf("%c", c);
    }

    int alignment = 0;

    for(int y = 1; y < MAX_ROWS-1; ++y) {
        for(int x = 1; x < MAX_COLS-1; ++x) {
            char c = droid->cells[y][x];

            if(c == '\n') {
                break;
            }

            if(c == '#') {
                if((droid->cells[y-1][x] == '#')
                        && (droid->cells[y+1][x] == '#')
                        && (droid->cells[y][x-1] == '#')
                        && (droid->cells[y][x+1] == '#')) {
                    alignment += (x * y);
                }
            }
        }
    }

    printf("Part1: aligment parameters = %d\n", alignment);
}

int main(int argc, char **argv)
{
    droid_t *droid = droid_new();

    if(argc >= 2) {
        if(intcode_read_from_file(&droid->soft, argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    droid_run(droid);

    droid_delete(droid);

    printf("done\n");
    return 0;
}
