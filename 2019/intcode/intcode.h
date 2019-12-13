#ifndef INTCODE_H
#define INTCODE_H

#include <stdint.h>
#include <inttypes.h>


/* == Configuration == */

#ifndef MEM_SIZE_MAX
#define MEM_SIZE_MAX  (64 * 1024)
#endif

#ifndef ENABLE_DUMP
#define ENABLE_DUMP   0
#endif

#ifndef ENABLE_TRACE
#define ENABLE_TRACE  0
#endif


/* == Types and data structures == */

typedef int64_t icword_t;
#define FMT_W  "%"PRId64
typedef int64_t icsize_t;
#define FMT_S  "%"PRId64

typedef enum {
    ERR_SUCCESS      = 0,
    ERR_WAIT_INPUT   = 1,
    ERR_YIELD_OUTPUT = 2,
    ERR_FAILURE      = -1,
} error_t;

typedef struct software{
    icword_t *mem;
    icword_t size;
    error_t (*get_input)(struct software *, icword_t *);
    error_t (*set_output)(struct software *, icword_t);
    icsize_t pc;
    icsize_t base;
} software_t;


/* == Utilities == */

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((n) / POW10[i]) % 10)

#define ARRAY_SIZE(ar)  ((icsize_t)(sizeof(ar)/sizeof((ar)[0])))

static const int POW10[6] = { 1, 10, 100, 1000, 10000, 100000 };


/* == Functions == */

void intcode_init(software_t *soft);

void intcode_destroy(software_t *soft);

/**
 * Read the given file into the intcode software.
 * Return number of positions, or -1 for failure.
 */
int intcode_read_from_file(software_t *soft, const char *filename);

/** Run the IntCode program. */
error_t intcode_run(software_t *soft);


#endif  /* INTCODE_H */
