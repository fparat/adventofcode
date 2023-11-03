#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include "intcode.h"

#define N "north\n"
#define E "east\n"
#define S "south\n"
#define W "west\n"
#define INV "inv\n"
#define HULL2SECU S S W S
#define SECU2HULL N E N N
#define TAKE(obj) "take " obj "\n"
#define DROP(obj) "drop " obj "\n"
#define BRING2SECU(obj) HULL2SECU DROP(obj) SECU2HULL
#define GATHER_OBJ(obj, from_hull, to_hull)  from_hull TAKE(obj) to_hull HULL2SECU DROP(obj) SECU2HULL

/* Gather all in security checkpoint */
const char *const GATHER_ALL =
    GATHER_OBJ("mouse", N, S)
    GATHER_OBJ("pointer", N N, S S)
    GATHER_OBJ("monolith", W, E)
    GATHER_OBJ("space law space brochure", W N W S, N E S E)
    GATHER_OBJ("food ration", W N W, E S E)
    GATHER_OBJ("sand", W S, N E)
    GATHER_OBJ("asterisk", W S S W, E N N E)
    GATHER_OBJ("mutex", W S S W S, N E N N E)
    HULL2SECU
;

typedef struct
{
    software_t soft;
    const char *input;
    size_t input_idx;
} droid_t;

#define TO_DROID(soft_ptr) ((droid_t *) (soft_ptr))


static error_t droid_get_input_interactive(software_t *soft, icword_t *value)
{
    (void) soft;
    *value = (icword_t) getchar();
    return ERR_SUCCESS;
}


static error_t droid_get_input_preset(software_t *soft, icword_t *value)
{
    droid_t *droid = TO_DROID(soft);

    char c = droid->input[droid->input_idx];

    *value = (icword_t) c;
    droid->input_idx++;
    putchar(c);

    if (droid->input[droid->input_idx] == '\0') {
        droid->soft.get_input = droid_get_input_interactive;
    }

    return ERR_SUCCESS;
}


static void droid_set_command_string(droid_t *droid, const char *command)
{
    droid->input = command;
    droid->input_idx = 0;
    droid->soft.get_input = droid_get_input_preset;
}


static error_t droid_set_output(struct software *soft, icword_t value)
{
    (void) soft;
    putchar((char) value);
    return ERR_SUCCESS;
}


static droid_t *droid_new()
{
    droid_t *droid = malloc(sizeof(droid_t));
    memset(droid, 0, sizeof(*droid));
    intcode_init(&droid->soft);
    droid->soft.get_input = droid_get_input_interactive;
    droid->soft.set_output = droid_set_output;
    return droid;
}


static void droid_delete(droid_t *droid)
{
    intcode_destroy(&droid->soft);
    free(droid);
}


static error_t droid_step(droid_t *droid)
{
    return intcode_step(&droid->soft);
}

static error_t droid_run(droid_t *droid)
{
    return intcode_run(&droid->soft);
}


static droid_t *droid_from_file(const char *path)
{
    droid_t *droid = droid_new();

    if(intcode_read_from_file(&droid->soft, path) != ERR_SUCCESS) {
        PANIC("Error reading input");
    }

    return droid;
}


const char *ITEMS[] = {
    "pointer",
    "mutex",
    "asterisk",
    "space law space brochure",
    "monolith",
    "mouse",
    "food ration",
    "sand",
};


static error_t droid_run_command(droid_t *droid, const char *command)
{
    error_t err = ERR_SUCCESS;

    droid_set_command_string(droid, command);
    while (err == ERR_SUCCESS && droid->soft.get_input != droid_get_input_interactive) {
        err = droid_step(droid);
    }

    return err;
}

/* Before calling this function gather all items in the security checkpoint */
static void droid_try_combinations(droid_t *droid)
{
    /* We have 8 items, each bit represent the presence of an item in the candidate combination.
     */

    uint32_t selected;
    char command[1024] = {0};

    for (selected = 0; selected < (1 << 8); ++selected) {
        /* take selected items*/
        for (size_t i = 0; i < ARRAY_SIZE(ITEMS); ++i) {
            if (selected & (1U << i)) {
                sprintf(command, "take %s\n", ITEMS[i]);
                if (droid_run_command(droid, command) != ERR_SUCCESS) {
                    goto end;
                }
            }
        }

        /* print the inventory before check */
        if (droid_run_command(droid, INV) != ERR_SUCCESS) {
            goto end;
        }

        /* try to pass the pressure check */
        if (droid_run_command(droid, E) != ERR_SUCCESS) {
            goto end;
        }

        /* drop items */
        for (size_t i = 0; i < ARRAY_SIZE(ITEMS); ++i) {
            if (selected & (1U << i)) {
                sprintf(command, "drop %s\n", ITEMS[i]);
                if (droid_run_command(droid, command) != ERR_SUCCESS) {
                    goto end;
                }
            }
        }
    }
    end:
    return;
}


int main(int argc, char **argv)
{
    droid_t *droid = droid_from_file(argc >= 2 ? argv[1] : "input");

    (void) droid_run;

    /* Part 1 */

    /* First, take a pen and paper, and explore the ship by manually entering the commands.
     * We also try to pick up the items to filter out the "special" ones.
     */
    /* droid_run(droid) */

    /* After we have a map, we can construct the GATHER_ALL string to brings all
     * items in the security checkpoint room.
     */

    /* Then we brute force all possible combinations until it works.
     * Intcode will return -1 when found, after printing the password
     */
    droid_run_command(droid, GATHER_ALL);
    droid_try_combinations(droid);

    droid_delete(droid);

    printf("done\n");
    return 0;
}
