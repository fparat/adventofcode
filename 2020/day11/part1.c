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

// return true if the state changed
static bool round(const seat_state_t state, seat_state_t next_state) {
    bool changed = false;
    int r, c;

    for(r = 0; state[r][0]; ++r) {
        for(c = 0; state[r][c]; ++c) {
            // copy state by default
            next_state[r][c] = state[r][c];

            if(r == 0 || c == 0 || state[r+1][0] == 0 || state[r][c+1] == 0) {
                // on a border, at least one side is empty
            } else {
                if(state[r][c] == SEAT_EMPTY) {
                    if(state[r-1][c-1] != SEAT_OCCUPIED
                            && state[r-1][c] != SEAT_OCCUPIED
                            && state[r-1][c+1] != SEAT_OCCUPIED
                            && state[r][c-1] != SEAT_OCCUPIED
                            && state[r][c+1] != SEAT_OCCUPIED
                            && state[r+1][c-1] != SEAT_OCCUPIED
                            && state[r+1][c] != SEAT_OCCUPIED
                            && state[r+1][c+1] != SEAT_OCCUPIED
                            ) {
                        next_state[r][c] = SEAT_OCCUPIED;
                        changed = true;
                    }
                } else if(state[r][c] == SEAT_OCCUPIED) {
                    int num_occupied = 0;
                    num_occupied += state[r-1][c-1] == SEAT_OCCUPIED;
                    num_occupied += state[r-1][c]   == SEAT_OCCUPIED;
                    num_occupied += state[r-1][c+1] == SEAT_OCCUPIED;
                    num_occupied += state[r]  [c-1] == SEAT_OCCUPIED;
                    num_occupied += state[r]  [c+1] == SEAT_OCCUPIED;
                    num_occupied += state[r+1][c-1] == SEAT_OCCUPIED;
                    num_occupied += state[r+1][c]   == SEAT_OCCUPIED;
                    num_occupied += state[r+1][c+1] == SEAT_OCCUPIED;
                    if(num_occupied >= 4) {
                        next_state[r][c] = SEAT_EMPTY;
                        changed = true;
                    }
                }
            }
        }
    }

    //print_seats(next_state);
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
    printf("Part 1: %d\n", num_occupied);


    return 0;
}
