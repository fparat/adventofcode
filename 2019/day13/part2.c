#include <string.h>
#include <unistd.h>
#include <ncurses.h>
#include "intcode.h"


#define DELAY      17000  // us, increase for slower, decrease for faster
#define ENABLE_AI  1

#define TILES_MAX  1024
#define FREE_GAME  2

typedef enum {
    TILE_EMPTY = 0,
    TILE_WALL = 1,
    TILE_BLOCK = 2,
    TILE_HPADDLE = 3,
    TILE_BALL = 4,
} tile_id_t;

static const char TILE_SHAPE[] = " #-=o";

typedef struct {
    int x;
    int y;
    tile_id_t id;
} tile_t;

typedef struct {
    software_t soft;
    tile_t tiles[TILES_MAX];
    int tiles_num;
    icword_t output[3];
    int output_idx;
    icword_t input;
    int input_valid;
    unsigned long score;
    unsigned long loop;
#ifdef ENABLE_AI
    int ai_previous_ball_x;
    int ai_previous_ball_y;
#endif
} arcade_t;

#define TO_ARCADE(soft_ptr)  ((arcade_t *) (soft_ptr))


static error_t arcade_get_input(software_t *soft, icword_t *value)
{
    arcade_t *arcade = TO_ARCADE(soft);

    if(!arcade->input_valid) {
        return ERR_WAIT_INPUT;
    }
    *value = arcade->input;
    arcade->input_valid = 0;

    return ERR_SUCCESS;
}


static error_t arcade_set_output(software_t *soft, icword_t value)
{
    arcade_t *arcade = TO_ARCADE(soft);

    if(arcade->output_idx >= 3) {
        PANIC("Need to read arcade output");
    }

    arcade->output[arcade->output_idx++] = value;

    return (arcade->output_idx >= 3) ? ERR_YIELD_OUTPUT : ERR_SUCCESS;
}


static void arcade_init(arcade_t *arcade)
{
    memset(arcade, 0, sizeof(*arcade));
    intcode_init(&arcade->soft);
    arcade->soft.get_input = arcade_get_input;
    arcade->soft.set_output = arcade_set_output;
}


static void arcade_destroy(arcade_t *arcade)
{
    intcode_destroy(&arcade->soft);
}


static void arcade_input(arcade_t *arcade, icword_t value)
{
    if(arcade->input_valid) {
        PANIC("Last input was not used");
    }
    arcade->input = value;
    arcade->input_valid = 1;
}


static void arcade_handle_key(arcade_t *arcade)
{
    int offset = 0;

    // Issue: there is a delay when a key is hold

    switch(getch())
    {
        case KEY_LEFT:
        case 'q':
            offset = -1;
            break;
        case KEY_RIGHT:
        case 'd':
            offset = 1;
            break;
        case ERR:
        default:
            break;
    }

    arcade_input(arcade, offset);
}


static void arcade_ai_update(arcade_t *arcade)
{
    int ball_x = 0, ball_y = 0;
    int paddle_x = 0;
    int found = 0;
    int ball_dir;
    int joydir = 0;

    // Find ball and paddle horizontal positions.
    // We assume there is only one of each.
    for(tile_t *tile = arcade->tiles; tile < &arcade->tiles[arcade->tiles_num]; tile++) {
        if(tile->id == TILE_BALL) {
            ball_x = tile->x;
            ball_y = tile->y;
            found++;
        } else if (tile->id == TILE_HPADDLE) {
            paddle_x = tile->x;
            found++;
        }
        if(found >= 2) {
            break;
        }
    }

    // Find ball direction: -1 is left, 1 is right, 0 is unknown
    if(arcade->loop == 0)  {
        ball_dir = 0;
    } else if (ball_x > arcade->ai_previous_ball_x) {
        ball_dir = 1;
    } else if (ball_x < arcade->ai_previous_ball_x) {
        ball_dir = -1;
    } else {
        ball_dir = 0;
    }

    // Decide action depending on ball moving direction and current position.
    if(ball_dir == 0) {
        joydir = 0;
    } else if(ball_dir < 0) {
        if(paddle_x >= ball_x) {
            joydir = -1;
        } else if (paddle_x < ball_dir - 1) {
            joydir = 1;
        }
    } else if(ball_dir > 0) {
        if(paddle_x < ball_x) {
            joydir = 1;
        } else if (paddle_x > ball_dir + 1) {
            joydir = -1;
        }
    } else {
        joydir = 0;
    }
    arcade_input(arcade, joydir);

    arcade->ai_previous_ball_x = ball_x;
    arcade->ai_previous_ball_y = ball_y;
}

static tile_t *arcade_get_tile(arcade_t *arcade, int x, int y)
{
    for(tile_t *tile = arcade->tiles; tile < &arcade->tiles[arcade->tiles_num]; tile++) {
        if(tile->x == x && tile->y == y) {
            return tile;
        }
    }
    return NULL;
}

static void arcade_write_tile(arcade_t *arcade, int x, int y, tile_id_t id)
{
    tile_t *tile = arcade_get_tile(arcade, x, y);

    if(!tile) {
        if(arcade->tiles_num >= TILES_MAX) {
            PANIC("Too many tiles");
        }
        tile = &arcade->tiles[arcade->tiles_num++];
        tile->x = x;
        tile->y = y;
    }
    tile->id = id;
}


static void arcade_handle_output(arcade_t *arcade)
{
    if(arcade->output_idx < 3) {
        PANIC("Incomplete arcade output");
    }

    if(arcade->output[0] == -1 && arcade->output[1] == 0) {
        // score update
        arcade->score = arcade->output[2];
    } else {
        // tile info
        arcade_write_tile(arcade, arcade->output[0], arcade->output[1], arcade->output[2]);
    }

    arcade->output_idx = 0;
}


static void arcade_display_refresh(arcade_t *arcade)
{
    clear();
    for(tile_t *tile = arcade->tiles; tile < &arcade->tiles[arcade->tiles_num]; tile++) {
        mvprintw(tile->y + 3, tile->x, "%c", TILE_SHAPE[tile->id]);
    }
    mvprintw(1, 1, "Score: %lu", arcade->score);
    refresh();
}

static void arcade_run(arcade_t *arcade)
{
    error_t error;
    tile_t tiles[TILES_MAX] = {0};
    int tiles_num = 0;
    int block_num = 0;
    int key;

    // Init ncurses
    newterm(NULL, stderr, stdin);
    noecho();
    nodelay(stdscr, TRUE);
    keypad(stdscr, TRUE);
    curs_set(FALSE);

    // Play
    arcade->soft.mem[0] = FREE_GAME;
    while(1) {
        switch(intcode_run(&arcade->soft)) {
            case ERR_SUCCESS:
                goto game_end;

            case ERR_WAIT_INPUT:
                arcade_display_refresh(arcade);
                usleep(DELAY);
#if ENABLE_AI
                arcade_ai_update(arcade);
#else
                arcade_handle_key(arcade);
#endif
                arcade->loop++;
                break;

            case ERR_YIELD_OUTPUT:
                arcade_handle_output(arcade);
                break;

            case ERR_FAILURE:
            default:
                PANIC("Something went wrong");
        }
    }
    game_end:

    // Cleanup ncurses
    endwin();

    printf("Score: %lu\n", arcade->score);
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
    arcade_destroy(&arcade);

    return 0;
}
