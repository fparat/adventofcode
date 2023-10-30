#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include "intcode.h"


typedef struct
{
    software_t soft;
    software_t baksoft;
    const char *script;
    size_t i;
} spring_t;

#define TO_SPRING(soft_ptr) ((spring_t *) (soft_ptr))


static error_t spring_get_input(software_t *soft, icword_t *value)
{
    spring_t *spring = TO_SPRING(soft);
    char c = spring->script[spring->i];
    if (c == 0) {
        PANIC("EOI");
    }

    *value = (icword_t) c;
    spring->i++;

    return ERR_SUCCESS;
}


static error_t spring_set_output(struct software *soft, icword_t value)
{
    (void) soft;

    if (value <= 0xFF) {
        putchar((char) value);
    } else {
        printf("Output: " FMT_W "\n", value);
    }

    return ERR_SUCCESS;
}


static spring_t *spring_new()
{
    spring_t *spring = malloc(sizeof(spring_t));
    memset(spring, 0, sizeof(*spring));
    intcode_init(&spring->soft);
    intcode_init(&spring->baksoft);
    spring->soft.get_input = spring_get_input;
    spring->soft.set_output = spring_set_output;
    return spring;
}


static void spring_delete(spring_t *spring)
{
    intcode_destroy(&spring->soft);
    intcode_destroy(&spring->baksoft);
    free(spring);
}


static void spring_backup(spring_t *spring)
{
    intcode_clone(&spring->baksoft, &spring->soft);
}


static void spring_restore(spring_t *spring)
{
    intcode_clone(&spring->soft, &spring->baksoft);
}


static void spring_run(spring_t *spring)
{
    error_t err;

    while((err = intcode_run(&spring->soft)) != ERR_SUCCESS) {
        assert(!"spring shouldn't yield");
    }
}


static spring_t *spring_from_file(const char *path)
{
    spring_t *spring = spring_new();

    if(intcode_read_from_file(&spring->soft, path) != ERR_SUCCESS) {
        PANIC("Error reading input");
    }

    spring_backup(spring);

    return spring;
}


static error_t spring_run_script(spring_t *spring, const char *script)
{
    spring_restore(spring);

    spring->script = script;
    spring->i = 0;
    spring_run(spring);

    return ERR_SUCCESS;
}


static char *read_to_string(const char *filename)
{
    char *buffer = NULL;
    long length;
    FILE *f = fopen(filename, "rb");

    if(!f) {
        PANIC("no input");
    }

    fseek(f, 0, SEEK_END);
    length = ftell(f);
    fseek(f, 0, SEEK_SET);
    buffer = malloc(length);
    if (!buffer) {
        PANIC("malloc failed");
    }
    fread(buffer, 1, length, f);
    fclose(f);

    return buffer;
}


int main(int argc, char **argv)
{
    spring_t *spring = spring_from_file(argc >= 2 ? argv[1] : "input");

    char *part1_script = read_to_string("part1.springscript");
    if (!part1_script) {
        PANIC("Failed to read part1 script");
    }

    spring_run_script(spring, part1_script);
    putchar('\n');

    free(part1_script);
    spring_delete(spring);

    printf("done\n");
    return 0;
}
