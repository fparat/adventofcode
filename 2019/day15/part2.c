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
    int depth;  // for part2
} tile_t;

typedef struct tile_t tile_t;


#define TILE_POOL_SIZE  (2 * 1024)

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


typedef bool (*callback_visit)(tile_t *visiting, void *user_data);
typedef void (*callback_backtrack)(tile_t *tile, void *user_data);

static bool was_visited(tile_t **visited, tile_t *target) {
    while(*visited) {
        if(*visited == target) {
            return true;
        }
        visited++;
    }
    return false;
}

static void push_visited(tile_t **visited, tile_t *target) {
    while(*visited) {
        visited++;
    }
    *visited = target;
}

typedef struct {
    tile_t *queue[TILE_POOL_SIZE];
    size_t in;
    size_t out;
} visited_queue_t;


static void visited_queue_push(visited_queue_t *queue, tile_t *visited) {
    queue->queue[queue->in] = visited;
    queue->in += 1;
    if(queue->in >= TILE_POOL_SIZE) {
        queue->in = 0;
    }
    if(queue->in == queue->out) {
        PANIC("Queue overflow");
    }
}

static tile_t *visited_queue_pop(visited_queue_t *queue) {
    if(queue->in == queue->out) {
        return NULL;  // empty
    } else {
        tile_t *popped = queue->queue[queue->out];
        queue->queue[queue->out] = NULL;
        queue->out++;
        if(queue->out >= TILE_POOL_SIZE) {
            queue->out = 0;
        }
        return popped;
    }
}


// Call tile_dfs_walk() instead if this function.
static void tile_dfs_walk_inner(
        tile_t *tile,
        callback_visit cb_visit,
        callback_backtrack cb_backtrack,
        void *user_data,
        tile_t **visited
) {
    if(cb_visit) {
        if(!cb_visit(tile, user_data)) {
            return;
        }
    }

    push_visited(visited, tile);

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
        callback_visit cb_visit,
        callback_backtrack cb_backtrack,
        void *user_data
) {
    // This entry function prepare the visited tile tracker then call the
    // function with the proper implementation.
    tile_t *visited[TILE_POOL_SIZE] = {0};
    tile_dfs_walk_inner(tile, cb_visit, cb_backtrack, user_data, visited);
}


// Call tile_bfs_walk() instead if this function.
static void tile_bfs_walk_inner(
        tile_t *tile,
        callback_visit cb_visit,
        void *user_data,
        tile_t **visited,
        visited_queue_t *queue
) {
    push_visited(visited, tile);
    visited_queue_push(queue, tile);

    tile_t *target;
    while((target = visited_queue_pop(queue))) {
        if(cb_visit) {
            if(!cb_visit(target, user_data)) {
                continue;
            }
        }

        for(direction_t direction = NORTH; direction <= EAST; direction++) {
            tile_t *next = tile_get_next(target, direction);
            if(!was_visited(visited, next)) {
                push_visited(visited, next);
                visited_queue_push(queue, next);
            }
        }
    }
}

// Breadth-First Search algorithm
// See tile_dfs_walk
static void tile_bfs_walk(
        tile_t *tile,
        callback_visit cb_visit,
        void *user_data
) {
    // This entry function prepare the visited tile tracker then call the
    // function with the proper implementation.
    tile_t *visited[TILE_POOL_SIZE] = {0};
    visited_queue_t queue = {0};
    tile_bfs_walk_inner(tile, cb_visit, user_data, visited, &queue);
}

typedef struct {
    software_t soft;
    tile_t *tiles;
    tile_t *position;
    direction_t move_command;
    droid_status_t status;
} droid_t;

#define TO_DROID(soft_ptr)  ((droid_t *) (soft_ptr))

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

typedef struct {
    droid_t *droid;
    direction_t move_stack[TILE_POOL_SIZE];
    tile_t *oxygen;
    int oxygen_distance;
    int max_queue_size;
} droid_walk_data_t;

static void move_stack_push(direction_t *queue, direction_t direction) {
    while(*queue) {
        queue++;
    }
    *queue = direction;
}

static direction_t move_stack_pop(direction_t *queue) {
    direction_t *last = queue;
    while(*queue) {
        last = queue++;
    }
    direction_t popped = *last;
    *last = 0;
    return popped;
}

static int move_stack_size(direction_t *queue) {
    int size = 0;
    while(*queue++) {
        size++;
    }
    return size;
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
    move_stack_push(data->move_stack, move_command);
    int queue_size = move_stack_size(data->move_stack);
    if(queue_size > data->max_queue_size) {
        data->max_queue_size = queue_size;
    }

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
                        move_stack_pop(data->move_stack);
                        break;
                    case STATUS_OXYGEN:
                        data->oxygen = visiting;
                        data->oxygen_distance = move_stack_size(data->move_stack);
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
            case ERR_WAIT_INPUT:
                return true;
            case ERR_FAILURE:
            default:
                PANIC("Something went wrong");
        }
    }

    end:
    return !backtrack;
}

static void droid_walk_backtrack_callback(tile_t *tile, void *user_data) {
    droid_walk_data_t *data = (droid_walk_data_t *) user_data;
    droid_t *droid = data->droid;

    (void) tile;

    direction_t direction;
    switch(move_stack_pop(data->move_stack)) {
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
}

#define DEPTH_MAX  TILE_POOL_SIZE

typedef struct {
    droid_t *droid;
    int depth_max;
} oxygen_fill_data_t;

static int neighbour_depth(tile_t *current, direction_t direction) {
    tile_t *neighbour = tile_get_neighbour(current, direction);
    if(neighbour->type == TILE_WALL) {
        return DEPTH_MAX;
    }
    return neighbour->depth;
}

static bool oxygen_fill_visit_callback(tile_t *visiting, void *user_data) {
    if(visiting->type == TILE_WALL) {
        return false;
    }

    oxygen_fill_data_t *data = user_data;

    int neighbour_min_depth = DEPTH_MAX;
    int depth;

    depth = neighbour_depth(visiting, NORTH);
    if(depth > 0 && depth < neighbour_min_depth) {
        neighbour_min_depth = depth;
    }
    depth = neighbour_depth(visiting, SOUTH);
    if(depth > 0 && depth < neighbour_min_depth) {
        neighbour_min_depth = depth;
    }
    depth = neighbour_depth(visiting, WEST);
    if(depth > 0 && depth < neighbour_min_depth) {
        neighbour_min_depth = depth;
    }
    depth = neighbour_depth(visiting, EAST);
    if(depth > 0 && depth < neighbour_min_depth) {
        neighbour_min_depth = depth;
    }

    if(neighbour_min_depth != DEPTH_MAX) {
        visiting->depth = neighbour_min_depth + 1;
        if(visiting->depth > data->depth_max) {
            data->depth_max = visiting->depth;
        }
        visiting->type = '0' + (visiting->depth % 10);
    }

    droid_t *droid = user_data;
    droid->position = visiting;

    return true;
}

static void droid_run(droid_t *droid) {
    droid_walk_data_t data = {
        .droid = droid,
        .move_stack = {0},
        .oxygen = NULL,
        .oxygen_distance = 0,
    };

    tile_dfs_walk(
        droid->tiles,
        droid_walk_visit_callback,
        droid_walk_backtrack_callback,
        &data
    );

    if(data.oxygen) {
        printf("Found oxygen at x=%d y=%d, distance=%d\n",
            data.oxygen->x, data.oxygen->y, data.oxygen_distance);
    } else {
        printf("Didn't find oxygen");
    }


    // Part 2: we have the full map of the ship, no need of the droid or Incode.
    // Use BFS algorithm for finding the fill time.

    data.oxygen->depth = 1;

    oxygen_fill_data_t oxygen_fill_data = {
        .droid = droid,
        .depth_max = 0,
    };

    tile_bfs_walk(
        data.oxygen,
        oxygen_fill_visit_callback,
        &oxygen_fill_data
    );

    printf("Fill time = %d\n", oxygen_fill_data.depth_max - 1);
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
