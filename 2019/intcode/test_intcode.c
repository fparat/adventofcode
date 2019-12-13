/**
 * Test program of the intcode (reimplementation of day 9)
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "intcode.h"

static icword_t boost_input = 0;

typedef struct boost_soft {
    software_t soft;  // keep first
    icword_t output;
    int output_is_set;
} boost_soft_t;

#define SOFT_TO_BOOST(soft_ptr)  ((boost_soft_t *)(soft_ptr))
#define BOOST_TO_SOFT(boost_ptr)  (&((boost_ptr)->soft))

static error_t boost_get_input(software_t *soft, icword_t *value)
{
    boost_soft_t *boost = SOFT_TO_BOOST(soft);
    (void) boost;
    *value = boost_input;
    return ERR_SUCCESS;
}

static error_t boost_set_output(software_t *soft, icword_t value)
{
    boost_soft_t *boost = SOFT_TO_BOOST(soft);
    boost->output = value;
    if(boost->output_is_set) {
        printf("Detected incorrect opcode: "FMT_W"\n", value);
    } else {
        boost->output_is_set = 1;
    }
    return ERR_SUCCESS;
}

static void boost_init(boost_soft_t *boost)
{
    software_t *soft = BOOST_TO_SOFT(boost);
    memset(boost, 0, sizeof(*boost));
    intcode_init(soft);
    soft->get_input = boost_get_input;
    soft->set_output = boost_set_output;
}

static void boost_destroy(boost_soft_t *boost)
{
    intcode_destroy(BOOST_TO_SOFT(boost));
}


static void boost_run(boost_soft_t *boost)
{
    if(intcode_run(BOOST_TO_SOFT(boost)) != ERR_SUCCESS) {
        PANIC("Something went wrong");
    }
    if(!boost->output_is_set) {
        PANIC("BOOST did not produce any output");
    }
}

static void read_input(boost_soft_t *boost)
{
    if(intcode_read_from_file(BOOST_TO_SOFT(boost), "../day09/input") != ERR_SUCCESS) {
        PANIC("Error reading input");
    }
}

int main(void)
{
    boost_soft_t boost = {0};

    boost_init(&boost);
    read_input(&boost);
    boost_input = 1;
    boost_run(&boost);
    if(boost.output != 2932210790) {
        PANIC("Test day 9 part 1 failure");
    }
    boost_destroy(&boost);

    boost_init(&boost);
    read_input(&boost);
    boost_input = 2;
    boost_run(&boost);
    if(boost.output != 73144) {
        PANIC("Test day 9 part 2 failure");
    }
    boost_destroy(&boost);

    printf("Test passed\n");
    return 0;
}
