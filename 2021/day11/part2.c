#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#include <ctype.h>

#define BOOM  "\033[1;31m"
#define BOUH  "\033[2m"
#define MEH   "\033[22;39m"

#define PANIC(msg)  do{ printf("PANIC: %s\n", (msg)); fflush(stdout); exit(1); }while(0)

static char *read_to_string(const char *filename)
{
    char *buffer = NULL;
    long length;
    FILE *f = fopen(filename, "rb");

    if(!f) {
        PANIC("no input");
    }

    fseek(f, 0, SEEK_END);
    length = ftell(f);
    fseek(f, 0, SEEK_SET);
    buffer = malloc(length);
    if (!buffer) {
        PANIC("malloc failed");
    }
    fread(buffer, 1, length, f);
    fclose(f);

    return buffer;
}

typedef struct
{
#define MAX_ROWS 32
#define MAX_COLS 32
    int oct[MAX_ROWS][MAX_COLS];
    int rows;
    int cols;
} grid_t;

static bool parse_octopuses(const char *input, grid_t *grid)
{
    char c;
    size_t row = 1, col = 1;

    while((c = *input++)) {
        if(isdigit(c)) {
            grid->oct[row][col++] = c - '0';
        } else if(c == '\n') {
            grid->cols = col;
            row++;
            col = 1;
        } else {
            PANIC("invalid input char");
        }

        if(row >= MAX_ROWS-1 || col >= MAX_COLS-1) {
            PANIC("grid too small");
        }
    }

    grid->rows = row;

    return true;
}

static inline void set_style(const grid_t *grid, int row, int col)
{
    bool is_border = row == 0 || row == grid->rows || col == 0 || col == grid->cols;

    if(is_border) {
        printf(BOUH);
    } else if(grid->oct[row][col] == 0) {
        printf(BOOM);
    }
}

static inline void clear_style(void)
{
    printf(MEH);
}

static void print_grid(const grid_t *grid)
{
    for(int row = 0; row <= grid->rows; ++row) {
        for(int col = 0; col <= grid->cols; ++col) {
            int v = grid->oct[row][col];
            set_style(grid, row, col);
            printf("%d", v);
            clear_style();
        }
        printf("\n");
    }
    printf("\n");
}

static void increment_level(grid_t *grid)
{
    for(int row = 1; row < grid->rows; ++row) {
        for(int col = 1; col < grid->cols; ++col) {
            grid->oct[row][col] += 1;
        }
    }
}

static int flash(grid_t *grid)
{
    int flashed = 0;

    for(int row = 1; row < grid->rows; ++row) {
        for(int col = 1; col <= grid->cols; ++col) {
            if(grid->oct[row][col] >= 10) {
                flashed++;
                grid->oct[row][col] = -100;  // avoid further flash
                grid->oct[row-1][col-1] += 1;
                grid->oct[row-1][col+0] += 1;
                grid->oct[row-1][col+1] += 1;
                grid->oct[row+0][col-1] += 1;
                grid->oct[row+0][col+0] += 1;
                grid->oct[row+0][col+1] += 1;
                grid->oct[row+1][col-1] += 1;
                grid->oct[row+1][col+0] += 1;
                grid->oct[row+1][col+1] += 1;
            }
        }
    }

    return flashed;
}

static void flash_reset(grid_t *grid)
{
    for(int row = 1; row < grid->rows; ++row) {
        for(int col = 1; col < grid->cols; ++col) {
            if(grid->oct[row][col] < 0) {
                grid->oct[row][col] = 0;
            }
        }
    }

    // reset borders
    for(int row = 0; row <= grid->rows; ++row) {
        grid->oct[row][0] = 0;
        grid->oct[row][grid->cols] = 0;
    }
    for(int col = 0; col <= grid->cols; ++col) {
        grid->oct[0][col] = 0;
        grid->oct[grid->rows][col] = 0;
    }
}

static void part1_2(const char *input)
{
    grid_t grid = {0};
    long int flashed = 0;
    int synchro_step = -1;

    parse_octopuses(input, &grid);
    print_grid(&grid);

    for(int step = 1;; ++step) {
        printf("step %d\n", step);
        increment_level(&grid);
        int step_flashed = 0;
        int substep_flashed = 0;
        while((substep_flashed = flash(&grid))) {
            step_flashed += substep_flashed;
        }
        flash_reset(&grid);

        print_grid(&grid);

        if(step_flashed == (grid.rows - 1) * (grid.cols - 1)) {
            if(synchro_step < 0) {
                synchro_step = step;
                if(step > 100) {
                    break;
                }
            }
        }

        if(step <= 100) {
            flashed += step_flashed;
        }
    }

    printf("Part 1: %ld\n", flashed);
    printf("Part 2: %d\n", synchro_step);
}

int main(int argc, char **argv)
{
    const char *input_filename = (argc >= 2) ? argv[1] : "input";
    char *input = read_to_string(input_filename);

    part1_2(input);

    return EXIT_SUCCESS;
}
