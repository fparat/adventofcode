#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include "intcode.h"

typedef struct
{
    software_t soft;
    software_t baksoft;
    icword_t input[2];
    size_t input_idx;
    icword_t out;
} drone_t;


#define TO_DRONE(soft_ptr) ((drone_t *) (soft_ptr))


static error_t drone_get_input(software_t *soft, icword_t *value)
{
    drone_t *drone = TO_DRONE(soft);

    assert(drone->input_idx < ARRAY_SIZE(drone->input));
    *value = drone->input[drone->input_idx++];


    return ERR_SUCCESS;
}


static error_t drone_set_output(struct software *soft, icword_t value)
{
    TO_DRONE(soft)->out = value;
    return ERR_SUCCESS;
}


static drone_t *drone_new()
{
    drone_t *drone = malloc(sizeof(drone_t));
    memset(drone, 0, sizeof(*drone));
    intcode_init(&drone->soft);
    intcode_init(&drone->baksoft);
    drone->soft.get_input = drone_get_input;
    drone->soft.set_output = drone_set_output;

    return drone;
}


static void drone_delete(drone_t *drone)
{
    intcode_destroy(&drone->soft);
    intcode_destroy(&drone->baksoft);
    free(drone);
}


static void drone_backup(drone_t *drone)
{
    intcode_clone(&drone->baksoft, &drone->soft);
}

static void drone_restore(drone_t *drone)
{
    intcode_clone(&drone->soft, &drone->baksoft);
}


static void drone_run(drone_t *drone)
{
    error_t err;

    while((err = intcode_run(&drone->soft)) != ERR_SUCCESS) {
        assert(!"drone shouldn't yield");
    }
}


static bool drone_is_pulled(drone_t *drone, icword_t x, icword_t y)
{
    drone_restore(drone);
    drone->input[0] = x;
    drone->input[1] = y;
    drone->input_idx = 0;
    drone_run(drone);
    return !!drone->out;
}


int main(int argc, char **argv)
{
    drone_t *drone = drone_new();

    if(argc >= 2) {
        if(intcode_read_from_file(&drone->soft, argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    drone_backup(drone);

    const int AREA_WIDTH = 50;
    const int AREA_HEIGHT = 50;

    int pulled_num = 0;

    for (int y = 0; y < AREA_HEIGHT; ++y) {
        for (int x = 0; x < AREA_WIDTH; ++x) {
            if (drone_is_pulled(drone, x, y)) {
                pulled_num += 1;
            }
        }
    }

    printf("Part 1: %d\n", pulled_num);

    drone_delete(drone);

    printf("done\n");
    return 0;
}
