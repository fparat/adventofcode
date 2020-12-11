#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define PANIC(msg)  do{ printf("PANIC: %s\n", (msg)); fflush(stdout); exit(1); }while(0)

static char *read_to_string(const char *filename) {
  char *buffer = 0;
  long length;
  FILE *f = fopen(filename, "rb");

  if (f) {
    fseek(f, 0, SEEK_END);
    length = ftell(f);
    fseek(f, 0, SEEK_SET);
    buffer = malloc(length);
    if (buffer) {
      fread(buffer, 1, length, f);
    }
    fclose(f);
  }

  return buffer;
}

#define SEAT_FLOOR '.'
#define SEAT_EMPTY 'L'
#define SEAT_OCCUPIED '#'

#define MAX_SEAT_ROWS  (4*1024)
#define MAX_SEAT_COLS  (4*1024)
static char seats[2][MAX_SEAT_ROWS][MAX_SEAT_COLS] = {0};

typedef char seat_state_t[MAX_SEAT_ROWS][MAX_SEAT_COLS];

static void print_seats(const seat_state_t seats) {
    int r, c;
    for(r = 0; seats[r][0]; ++r) {
        for(c = 0; seats[r][c]; ++c) {
            printf("%c", seats[r][c]);
        }
        printf("\n");
    }
    printf("\n");
}

static char look(const seat_state_t seats, int r, int c, int dr, int dc) {
    char seen = SEAT_FLOOR;

    r += dr;
    c += dc;
    while(r >= 0 && c >= 0 && seats[r][c]) {
        seen = seats[r][c];
        if(seen == SEAT_EMPTY || seen == SEAT_OCCUPIED) {
            return seen;
        }
        r += dr;
        c += dc;
    }

    return seen;
}

// return true if the state changed
static bool round(const seat_state_t state, seat_state_t next_state) {
    bool changed = false;
    int r, c;

    //print_seats(state);

    for(r = 0; state[r][0]; ++r) {
        for(c = 0; state[r][c]; ++c) {
            // copy state by default
            next_state[r][c] = state[r][c];

            char neighbours[8] = {0};
            neighbours[0] = look(state, r, c, -1, -1);
            neighbours[1] = look(state, r, c, -1,  0);
            neighbours[2] = look(state, r, c, -1,  1);
            neighbours[3] = look(state, r, c,  0, -1);
            neighbours[4] = look(state, r, c,  0,  1);
            neighbours[5] = look(state, r, c,  1, -1);
            neighbours[6] = look(state, r, c,  1,  0);
            neighbours[7] = look(state, r, c,  1,  1);

            if(state[r][c] == SEAT_EMPTY) {
                bool ok = true;
                for(int n = 0; n < 8; ++n) {
                    if(neighbours[n] == SEAT_OCCUPIED) {
                        ok = false;
                        break;
                    }
                }
                if(ok) {
                    next_state[r][c] = SEAT_OCCUPIED;
                    changed = true;
                }
            } else if(state[r][c] == SEAT_OCCUPIED) {
                int num_occupied = 0;
                for(int n = 0; n < 8; ++n) {
                    num_occupied += (neighbours[n] == SEAT_OCCUPIED);
                }
                if(num_occupied >= 5) {
                    next_state[r][c] = SEAT_EMPTY;
                    changed = true;
                }
            }
        }
    }

    return changed;
}


static int count_occupied(const seat_state_t seats) {
    int r, c;
    int num = 0;
    for(r = 0; seats[r][0]; ++r) {
        for(c = 0; seats[r][c]; ++c) {
            num += (seats[r][c] == SEAT_OCCUPIED);
        }
    }
    return num;
}


int main(int argc, char **argv) {
    const char *input_filename = (argc >= 2) ? argv[1] : "input";
    char *input = read_to_string(input_filename);

    const char *s;
    size_t r = 1, c = 1;
    for(s = input; *s != '\0'; ++s) {
        if(*s == '\n' || *s == '\r') {
            // fill first and last column with floor
            seats[0][r][0] = SEAT_FLOOR;
            seats[0][r][c] = SEAT_FLOOR;

            r++;
            c = 1;
        } else {
            seats[0][r][c] = *s;
            c++;
        }
    }
    // fill first and last row with floor
    for(c = 0; seats[0][1][c]; ++c) {
        seats[0][0][c] = SEAT_FLOOR;
        seats[0][r][c] = SEAT_FLOOR;
    }

    int i = 0;
    int i2 = 1;
    while(round(seats[i], seats[i2])) {
        i2 = i;
        i = (i + 1) & 1;
    }

    int num_occupied = count_occupied(seats[0]);
    printf("Part 2: %d\n", num_occupied);


    return 0;
}
