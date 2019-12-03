#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

#define WIRE_NUM (2)
#define WIRE_SIZE_MAX (512 * 1024)

#define ABS(x)  (((x) >= 0) ? (x) : -(x))
#define DISTANCE(pos) (ABS((pos).x) + ABS((pos).y))

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

typedef struct
{
    char direction;
    int distance;
} Move;

typedef struct
{
    Move moves[1024];
    int size;
} Wire;

typedef struct
{
    int x;
    int y;
} Position;

/* Return -1 for failure */
static int read_input(const char *filename, Wire *wires)
{
    FILE *f;
    char direction;
    int distance;
    int n;

    f = fopen(filename, "rb");
    if(!f) {
        PANIC("Could not read file");
    }

    wires->size = 0;

    while(1) {
        n = fscanf(f, "%c%d,", &direction, &distance);
        if((n == 1) && (direction == '\n')) {
            // newline: next wire
            wires++;
            wires->size = 0;
        } else if(n == 2) {
            // new move
            wires->moves[wires->size].direction = direction;
            wires->moves[wires->size].distance = distance;
            wires->size++;
        } else {
            break;
        }
    }

    for(int i = 0; i < wires->size; i++)
    {
        printf("%c-%d|", wires->moves[i].direction, wires->moves[i].distance);
    }
    printf("\n");

    fclose(f);

    return 0;
}

int main(int argc, char **argv)
{
    Wire wires[WIRE_NUM+1] = {0};
    Position pos1[WIRE_SIZE_MAX] = {0};
    Position *pos;
    Position pos2 = {0};
    Move *move;
    int len1;
    int m;
    int dx, dy;
    int distance = INT_MAX;

    if(argc < 2) {
        PANIC("Please give input file in argument");
    }

    if(read_input(argv[1], wires) != 0) {
        PANIC("Input read error");
    }

    // Draw first wire
    pos = pos1;
    for(m = 0; m < wires[0].size; ++m) {
        move = &wires[0].moves[m];
        while(move->distance-- > 0) {
            dx = (move->direction == 'R') ? 1 : (move->direction == 'L') ? -1 : 0;
            dy = (move->direction == 'U') ? 1 : (move->direction == 'D') ? -1 : 0;
            pos[1].x = pos[0].x + dx;
            pos[1].y = pos[0].y + dy;
            pos++;
        }
    }
    len1 = pos - pos1;

    // Draw second wire, looking for close intersection with 1st wire
    for(m = 0; m < wires[1].size; ++m) {
        move = &wires[1].moves[m];
        while(move->distance-- > 0) {
            dx = (move->direction == 'R') ? 1 : (move->direction == 'L') ? -1 : 0;
            dy = (move->direction == 'U') ? 1 : (move->direction == 'D') ? -1 : 0;
            pos2.x = pos2.x + dx;
            pos2.y = pos2.y + dy;
            if(DISTANCE(pos2) < distance) {
                for(pos = pos1; pos < &pos1[len1]; ++pos) {
                    if((pos->x == pos2.x) && (pos->y == pos2.y)) {
                        if(ABS(pos2.x) + ABS(pos2.y) < distance) {
                            distance = ABS(pos2.x) + ABS(pos2.y);
                        }
                    }
                }
            }
        }
    }

    printf("Result: %d\n", distance);

    return 0;
}
