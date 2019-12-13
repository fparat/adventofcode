#include <string.h>
#include "intcode.h"


#define TILES_MAX  1024


typedef enum {
    TILE_EMPTY = 0,
    TILE_WALL = 1,
    TILE_BLOCK = 2,
    TILE_HPADDLE = 3,
    TILE_BALL = 4,
} tile_id_t;

typedef struct {
    int x;
    int y;
    tile_id_t id;
} tile_t;

typedef struct {
    software_t soft;
    icword_t output[3];
    int output_idx;
} arcade_t;

#define TO_ARCADE(soft_ptr)  ((arcade_t *) (soft_ptr))


error_t arcade_get_input(software_t *soft, icword_t *value)
{
    (void) soft;
    (void) value;
    return ERR_FAILURE;
}

error_t arcade_set_output(software_t *soft, icword_t value)
{
    arcade_t *arcade = TO_ARCADE(soft);

    if(arcade->output_idx >= 3) {
        PANIC("Need to read arcade output");
    }

    arcade->output[arcade->output_idx++] = value;

    return (arcade->output_idx >= 3) ? ERR_YIELD_OUTPUT : ERR_SUCCESS;
}

void arcade_init(arcade_t *arcade)
{
    memset(arcade, 0, sizeof(*arcade));
    intcode_init(&arcade->soft);
    arcade->soft.get_input = arcade_get_input;
    arcade->soft.set_output = arcade_set_output;
}

void arcade_destroy(arcade_t *arcade)
{
    intcode_destroy(&arcade->soft);
}

void arcade_read_tile(arcade_t *arcade, tile_t *tile)
{
    if(arcade->output_idx < 3) {
        PANIC("Not enough values for tile");
    }
    tile->x = arcade->output[0];
    tile->y = arcade->output[1];
    tile->id = arcade->output[2];
    arcade->output_idx = 0;

}

void arcade_run(arcade_t *arcade)
{
    error_t error;
    tile_t tiles[TILES_MAX] = {0};
    int tiles_num = 0;
    int block_num = 0;

    while((error = intcode_run(&arcade->soft)) != ERR_SUCCESS) {
        if(error == ERR_YIELD_OUTPUT) {
            arcade_read_tile(arcade, &tiles[tiles_num++]);
            if(tiles_num >= TILES_MAX) {
                PANIC("Too many tiles");
            }
        } else {
            PANIC("Something went wrong");
        }
    }

    for(int i = 0; i < ARRAY_SIZE(tiles); i++) {
        if(tiles[i].id == TILE_BLOCK) {
            block_num++;
        }
    }

    printf("Result: %d\n", block_num);
}


int main(int argc, char **argv)
{
    arcade_t arcade = {0};
    arcade_init(&arcade);

    if(argc >= 2) {
        if(intcode_read_from_file(&arcade.soft, argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    arcade_run(&arcade);

    //printf("Result: "FMT_W"\n", arcade.output);

    arcade_destroy(&arcade);

    return 0;
}
