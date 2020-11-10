#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "intcode.h"


#ifndef ENABLE_DRAW
#define ENABLE_DRAW  0
#endif
#if ENABLED_DRAW
#include <unistd.h>
#endif


#define ABS(x)  ((x) > 0 ? (x) : -(x))


typedef enum {
    DIRECTION_NONE = 0,
    NORTH = 1,
    SOUTH = 2,
    WEST  = 3,
    EAST  = 4
} direction_t;


typedef enum {
    STATUS_WALL   = 0,
    STATUS_MOVE   = 1,
    STATUS_OXYGEN = 2
} droid_status_t;


typedef enum {
    TILE_UNKNOWN  = '?',
    TILE_FLOOR    = '.',
    TILE_WALL     = '#',
    TILE_DROID    = 'D',
    TILE_OXYGEN   = 'O'
} tile_type_t;


typedef struct tile_t{
    int x;
    int y;
    tile_type_t type;
    struct tile_t *north;
    struct tile_t *south;
    struct tile_t *west;
    struct tile_t *east;
} tile_t;

typedef struct tile_t tile_t;


#define TILE_POOL_SIZE  (256 * 1024)

static tile_t tile_pool[TILE_POOL_SIZE] = {0};
static size_t tile_pool_next = 0;

static tile_t *tile_new(int x, int y, tile_type_t type) {
    if(tile_pool_next >= TILE_POOL_SIZE) {
        PANIC("Tile pool empty");
    }
    tile_t *tile = &tile_pool[tile_pool_next++];
    tile->x = x;
    tile->y = y;
    tile->type = type;
    return tile;
}

static tile_t *tile_find(int x, int y) {
    for(size_t i = 0; i < tile_pool_next; ++i) {
        if((tile_pool[i].x == x) && (tile_pool[i].y == y)) {
            return &tile_pool[i];
        }
    }
    return NULL;
}


static tile_t *tile_get_neighbour(tile_t *origin, direction_t direction) {
    int x = origin->x + (direction == EAST) - (direction == WEST);
    int y = origin->y + (direction == NORTH) - (direction == SOUTH);

    tile_t *tile;

    tile = tile_find(x, y);
    if(!tile) {
        tile = tile_new(x, y, TILE_UNKNOWN);
        if(!tile) {
            PANIC("Cannot create new tile");
        }
    }

    switch(direction) {
        case NORTH: origin->north = tile; tile->south = origin; break;
        case SOUTH: origin->south = tile; tile->north = origin; break;
        case WEST:  origin->west =  tile; tile->east =  origin; break;
        case EAST:  origin->east =  tile; tile->west =  origin; break;
        default: PANIC("Invalid direction");
    }


    return tile;
}

static tile_t *tile_get_next(tile_t *tile, direction_t direction) {
    tile_t *next;
    switch(direction) {
        case NORTH: next = tile->north; break;
        case SOUTH: next = tile->south; break;
        case WEST:  next = tile->west;  break;
        case EAST:  next = tile->east;  break;
        default: return NULL;
    }
    return next ? next : tile_get_neighbour(tile, direction);
}


#define DRAW_MAP_SIZE  43   // keep odd
#define DRAW_MAP_UP    (DRAW_MAP_SIZE / 2)
#define DRAW_MAP_DOWN  (-(DRAW_MAP_SIZE / 2))
#define DRAW_MAP_LEFT  (-(DRAW_MAP_SIZE / 2))
#define DRAW_MAP_RIGHT (DRAW_MAP_SIZE / 2)
#define POS_TO_DRAW_X(x)  ((x) + (DRAW_MAP_SIZE / 2))
#define POS_TO_DRAW_Y(y)  ((y) + (DRAW_MAP_SIZE / 2))

typedef struct {
    software_t soft;
    tile_t *tiles;
    tile_t *position;
    direction_t move_command;
    droid_status_t status;
    tile_t *oxygen;
    int oxygen_distance;
} droid_t;

#define TO_DROID(soft_ptr)  ((droid_t *) (soft_ptr))

#define POS_IN_DRAW_RANGE(x, y)  \
  (((x) <= DRAW_MAP_RIGHT) \
    && ((x) >= DRAW_MAP_LEFT) \
    && ((y) <= DRAW_MAP_UP) \
    && ((y) >= DRAW_MAP_DOWN))


typedef bool (*callback_dfs_visit)(tile_t *visiting, void *user_data);
typedef void (*callback_dfs_backtrack)(tile_t *tile, void *user_data);


static bool was_visited(tile_t **visited, tile_t *target) {
    while(*visited) {
        if(*visited == target) {
            return true;
        }
        visited++;
    }
    return false;
}

static void set_visited(tile_t **visited, tile_t *target) {
    while(*visited) {
        visited++;
    }
    *visited = target;
}

typedef struct {
    droid_t *droid;
    direction_t move_queue[TILE_POOL_SIZE];
} droid_walk_data_t;

static void move_queue_push(direction_t *queue, direction_t direction) {
    while(*queue) {
        queue++;
    }
    *queue = direction;
}

static direction_t move_queue_pop(direction_t *queue) {
    direction_t *last = queue;
    while(*queue) {
        last = queue++;
    }
    direction_t popped = *last;
    *last = 0;
    return popped;
}

static int move_queue_size(direction_t *queue) {
    int size = 0;
    while(*queue++) {
        size++;
    }
    return size;
}

static void tile_dfs_walk_inner(
        tile_t *tile,
        callback_dfs_visit cb_visit,
        callback_dfs_backtrack cb_backtrack,
        void *user_data,
        tile_t **visited
) {
    if(cb_visit) {
        if(!cb_visit(tile, user_data)) {
            return;
        }
    }

    set_visited(visited, tile);

    for(direction_t direction = NORTH; direction <= EAST; direction++) {
        tile_t *next = tile_get_next(tile, direction);
        if(!was_visited(visited, next)) {
            tile_dfs_walk_inner(next, cb_visit, cb_backtrack, user_data, visited);
        }
    }

    cb_backtrack(tile, user_data);
}

// Depth-First Search algorithm
// For each visited tile the callback cb_visit is called, then the
// algorithm continue if the return value of the callback is true.
// During backtracking cb_backtrack is called.
static void tile_dfs_walk(
        tile_t *tile,
        callback_dfs_visit cb_visit,
        callback_dfs_backtrack cb_backtrack,
        void *user_data
) {
    // This entry function prepare the visited tile tracker then call the
    // function with the proper implementation.
    tile_t *visited[TILE_POOL_SIZE] = {0};
    tile_dfs_walk_inner(tile, cb_visit, cb_backtrack, user_data, visited);
}


static void droid_draw_map(droid_t *droid) {
#if ENABLE_DRAW
    char map[DRAW_MAP_SIZE][DRAW_MAP_SIZE] = {0};
    memset(map, ' ', sizeof(map));

    for(size_t tile_idx = 0; tile_idx < tile_pool_next; tile_idx++) {
        const tile_t *tile = &tile_pool[tile_idx];
        if(POS_IN_DRAW_RANGE(tile->x, tile->y)) {
            map[POS_TO_DRAW_X(tile->x)][POS_TO_DRAW_Y(tile->y)] = tile->type;
        }
    }

    if(POS_IN_DRAW_RANGE(droid->position->x, droid->position->y)) {
        map[POS_TO_DRAW_X(droid->position->x)][POS_TO_DRAW_Y(droid->position->y)] = TILE_DROID;
    }

    printf("    ");
    for(int x = 0; x < DRAW_MAP_SIZE; ++x) {
        printf("%d", (int)ABS(x + DRAW_MAP_DOWN) % 10);
    }
    printf("\n");
    for(int y = DRAW_MAP_SIZE - 1; y >= 0; --y) {
        printf("%3d ", y + DRAW_MAP_DOWN);
        for(int x = 0; x < DRAW_MAP_SIZE; ++x) {
            printf("%c", map[x][y]);
        }
        printf("\n");
    }
    printf("\n");

    usleep(33333);
#else
    (void) droid;
#endif
}


static error_t droid_get_input(software_t *soft, icword_t *value)
{
    droid_t *droid = TO_DROID(soft);
    *value = droid->move_command;
    return ERR_SUCCESS;
}


static error_t droid_set_output(software_t *soft, icword_t value)
{
    droid_t *droid = TO_DROID(soft);
    droid->status = (int) value;
    return ERR_YIELD_OUTPUT;
}


static void droid_init(droid_t *droid)
{
    memset(droid, 0, sizeof(*droid));
    intcode_init(&droid->soft);
    droid->soft.get_input = droid_get_input;
    droid->soft.set_output = droid_set_output;

    // assume the droid starts on the floor
    tile_t *origin_tile = tile_new(0, 0, TILE_FLOOR);
    droid->tiles = origin_tile;
    droid->position = origin_tile;
}


static void droid_destroy(droid_t *droid)
{
    intcode_destroy(&droid->soft);
}


static bool droid_walk_visit_callback(tile_t *visiting, void *user_data) {
    droid_walk_data_t *data = (droid_walk_data_t *) user_data;
    droid_t *droid = data->droid;
    direction_t move_command;

    if(visiting == droid->position->north) {
        move_command = NORTH;
    } else if(visiting == droid->position->south) {
        move_command = SOUTH;
    } else if(visiting == droid->position->west) {
        move_command = WEST;
    } else if(visiting == droid->position->east) {
        move_command = EAST;
    } else {
        printf("Unconnected tile\n");
        return true;
    }

    droid->move_command = move_command;
    move_queue_push(data->move_queue, move_command);

    // Loop the Intcode machine until it yields an output.
    error_t error;
    bool backtrack = false;
    while(1) {
        error = intcode_run(&data->droid->soft);
        switch(error) {
            case ERR_SUCCESS:
                PANIC("Unexpected success");
                break;
            case ERR_YIELD_OUTPUT:
                switch(droid->status) {
                    case STATUS_WALL:
                        visiting->type = TILE_WALL;
                        backtrack = true;
                        move_queue_pop(data->move_queue);
                        break;
                    case STATUS_OXYGEN:
                        droid->oxygen = visiting;
                        droid->oxygen_distance = move_queue_size(data->move_queue);
                        /* fallthrough */
                    case STATUS_MOVE:
                        visiting->type = (droid->status == STATUS_MOVE) ? TILE_FLOOR : TILE_OXYGEN;
                        droid->position = visiting;
                        backtrack = false;
                        break;
                    default:
                        return ERR_FAILURE;
                }
                goto end;
                droid->position = visiting;
                break;
            case ERR_WAIT_INPUT:
                return true;
            case ERR_FAILURE:
            default:
                PANIC("Something went wrong");
        }
    }

    end:
    droid_draw_map(droid);
    return !backtrack;
}

static void droid_walk_backtrack_callback(tile_t *tile, void *user_data) {
    droid_walk_data_t *data = (droid_walk_data_t *) user_data;
    droid_t *droid = data->droid;

    (void) tile;

    direction_t direction;
    switch(move_queue_pop(data->move_queue)) {
        case NORTH: direction = SOUTH; break;
        case SOUTH: direction = NORTH; break;
        case WEST: direction = EAST; break;
        case EAST: direction = WEST; break;
        default: return;  // empty move queue, probably returned to start point
    }
    droid->move_command = direction;

    error_t error;
    while((error = intcode_run(&droid->soft)) != ERR_YIELD_OUTPUT) {
        if((error != ERR_YIELD_OUTPUT) || (droid->status != STATUS_MOVE)) {
            PANIC("Unexpected state when backtracking");
        }
        if(droid->position->type != TILE_FLOOR) {
            PANIC("Unexpected tile type when backtracking");
        }
    }

    droid->position = tile_get_neighbour(droid->position, direction);

    droid_draw_map(droid);
}

static void droid_run(droid_t *droid) {
    droid_walk_data_t walk_data = {
        .droid = droid,
        .move_queue = {0},
    };

    tile_dfs_walk(
        droid->tiles,
        droid_walk_visit_callback,
        droid_walk_backtrack_callback,
        &walk_data
    );

    if(droid->oxygen) {
        printf("Found oxygen at x=%d y=%d, distance=%d\n",
            droid->oxygen->x, droid->oxygen->y, droid->oxygen_distance);
    } else {
        printf("Didn't find oxygen");
    }
}


int main(int argc, char **argv)
{
    droid_t droid = {0};
    droid_init(&droid);

    if(argc >= 2) {
        if(intcode_read_from_file(&droid.soft, argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    droid_run(&droid);

    droid_destroy(&droid);

    printf("done\n");
    return 0;
}
