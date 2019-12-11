#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((n) / POW10[i]) % 10)

#define ARRAY_SIZE(ar)  ((icsize_t)(sizeof(ar)/sizeof((ar)[0])))

static const int POW10[6] = { 1, 10, 100, 1000, 10000, 100000 };

typedef int64_t icword_t;
#define FMT_W  "%"PRId64
typedef int64_t icsize_t;
#define FMT_S  "%"PRId64

#define OP_ADD          1
#define OP_MUL          2
#define OP_INPUT        3
#define OP_OUTPUT       4
#define OP_JMP_TRUE     5
#define OP_JMP_FALSE    6
#define OP_LESS         7
#define OP_EQUAL        8
#define OP_BASE_ADD     9
#define OP_HLT          99

#define MODE_POSITION   0
#define MODE_IMMEDIATE  1
#define MODE_RELATIVE   2

#define OP(op)       ((op) % 100)
#define MODE(op, i)  DIGIT((op), (i) + 2)

#define MEM_SIZE_MAX  (64 * 1024)

typedef enum {
    ERR_SUCCESS      = 0,
    ERR_WAIT_INPUT   = 1,
    ERR_YIELD_OUTPUT = 2,
    ERR_FAILURE      = -1,
} error_t;

#define ENABLE_DUMP   0
#define ENABLE_TRACE  0

#if ENABLE_TRACE
#define TRACE(msg)  do{ printf msg ; fflush(stdout); }while(0)
#else
#define TRACE(msg)
#endif


typedef struct software{
    icword_t *mem;
    icword_t size;
    error_t (*get_input)(struct software *, icword_t *);
    error_t (*set_output)(struct software *, icword_t);
    icsize_t pc;
    icsize_t base;
} software_t;

error_t soft_get_input_unimplemented(struct software *soft, icword_t *value)
{
    (void) soft;
    (void) value;
    PANIC("Unimplemented 'get_input' function");
    return ERR_FAILURE;
}

error_t soft_set_output_unimplemented(struct software *soft, icword_t value)
{
    (void) soft;
    (void) value;
    PANIC("Unimplemented 'set_input' function");
    return ERR_FAILURE;
}

static void software_init(software_t *soft)
{
    memset(soft, 0, sizeof(*soft));
    soft-> mem = malloc(MEM_SIZE_MAX);
    soft->get_input = soft_get_input_unimplemented;
    soft->set_output = soft_set_output_unimplemented;
}

static void software_destroy(software_t *soft)
{
    free(soft->mem);
}


static void dump(const icword_t *buf, icsize_t len)
{
#if ENABLE_DUMP
    // to redo
    (void) buf;
    (void) len;
#else
    (void) buf;
    (void) len;
#endif  /* ENABLE_DUMP */
}


static icword_t param_value(const software_t *soft, int idx)
{
    icword_t param = soft->mem[soft->pc+1+idx];
    int mode = MODE(soft->mem[soft->pc], idx);
    icword_t value;

    TRACE(("param "FMT_W", mode %d ", param, mode));

    switch(mode) {
        case MODE_POSITION:
            TRACE(("(read @"FMT_W")", param));
            value = soft->mem[param];
            break;
        case MODE_IMMEDIATE:
            value = param;
            break;
        case MODE_RELATIVE:
            TRACE(("(read @"FMT_S"+"FMT_W"="FMT_W")", soft->base, param, soft->base + param));
            value = soft->mem[soft->base + param];
            break;
        default:
            PANIC("Invalid mode");
    }
    TRACE((" -> "FMT_W"\n", value));
    return value;
}


static icsize_t param_pos(const software_t *soft, int idx)
{
    icword_t param = soft->mem[soft->pc+1+idx];
    int mode = MODE(soft->mem[soft->pc], idx);
    icsize_t pos;

    TRACE(("write_pos  "FMT_W", mode %d ", param, mode));

    switch(mode) {
        case MODE_POSITION:
            TRACE(("(write @"FMT_W")", param));
            pos = param;
            break;
        case MODE_IMMEDIATE:
            PANIC("lvalue cannot be in 'immediate' mode");
            break;
        case MODE_RELATIVE:
            pos = soft->base + param;
            TRACE(("(write @"FMT_S"+"FMT_W"="FMT_S")", soft->base, param, pos));
            break;
        default:
            PANIC("Invalid mode");
    }
    TRACE((" -> "FMT_S"\n", pos));
    return pos;
}


static int param_num(int op)
{
    switch(op) {
        case OP_ADD:       return 3;
        case OP_MUL:       return 3;
        case OP_INPUT:     return 1;
        case OP_OUTPUT:    return 1;
        case OP_JMP_TRUE:  return 2;
        case OP_JMP_FALSE: return 2;
        case OP_LESS:      return 3;
        case OP_EQUAL:     return 3;
        case OP_BASE_ADD:  return 1;
        case OP_HLT:       return 0;
        default:           PANIC("Unexpected op");
    }
}

static error_t run_program(software_t *soft)
{
    icword_t *mem = soft->mem;
    icsize_t size = soft->size;
    icword_t op;
    int pnum;
    icword_t param[8] = {0};
    icsize_t offset;
    int i;
    icword_t value;
    icsize_t write_pos;
    error_t error = ERR_SUCCESS;

    while((error == ERR_SUCCESS) && (OP(mem[soft->pc]) != OP_HLT)) {
        TRACE(("-----\n"));
        TRACE(("pc="FMT_S", ["FMT_W", "FMT_W", "FMT_W", "FMT_W"]\n",
            soft->pc, mem[soft->pc], mem[soft->pc+1], mem[soft->pc+2], mem[soft->pc+3]));

        dump(mem, soft->size);

        op = OP(mem[soft->pc]);
        pnum = param_num(op);
        for(i = 0; i < pnum; ++i) {
            param[i] = param_value(soft, i);
        }
        offset = pnum + 1;

        TRACE(("op="FMT_W", params: "FMT_W", "FMT_W"\n", op, param[0], param[1]));

        switch(op) {
            case OP_ADD:
                write_pos = param_pos(soft, 2);
                TRACE(("ADD: "FMT_W" + "FMT_W" -> ("FMT_S")\n", param[0], param[1], write_pos));
                mem[write_pos] = param[0] + param[1];
                break;

            case OP_MUL:
                write_pos = param_pos(soft, 2);
                TRACE(("MUL: "FMT_W" * "FMT_W" -> ("FMT_S")\n", param[0], param[1], write_pos));
                mem[write_pos] = param[0] * param[1];
                break;

            case OP_INPUT:
                switch(soft->get_input(soft, &value)) {
                    case ERR_SUCCESS:
                        write_pos = param_pos(soft, 0);
                        TRACE(("INPUT: "FMT_W" -> ("FMT_S")\n", value, write_pos));
                        mem[write_pos] = value;
                        break;
                    case ERR_WAIT_INPUT:
                        TRACE(("WAIT INPUT\n"));
                        return ERR_WAIT_INPUT;
                    case ERR_FAILURE:
                    default:
                        PANIC("Critical error");
                        break;
                }
                break;

            case OP_OUTPUT:
                TRACE(("OUTPUT: "FMT_W"\n", param[0]));
                error = soft->set_output(soft, param[0]);
                break;

            case OP_JMP_TRUE:
                TRACE(("JMPTRUE: "FMT_W"", param[0]));
                if(param[0]) {
                    TRACE((" -> true @"FMT_W"\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> false\n"));
                }
                break;

            case OP_JMP_FALSE:
                TRACE(("JMPTRUE: "FMT_W"", param[0]));
                if(!param[0]) {
                    TRACE((" -> false @"FMT_W"\n", param[1]));
                    soft->pc = param[1];
                    offset = 0;
                } else {
                    TRACE((" -> true\n"));
                }
                break;

            case OP_LESS:
                write_pos = param_pos(soft, 2);
                TRACE(("LESS: "FMT_W" < "FMT_W" -> "FMT_S"\n", param[0], param[1], write_pos));
                mem[write_pos] = (param[0] < param[1]) ? 1 : 0;
                break;

            case OP_EQUAL:
                write_pos = param_pos(soft, 2);
                TRACE(("EQUAL: "FMT_W" == "FMT_W" -> "FMT_S"\n", param[0], param[1], write_pos));
                mem[write_pos] = (param[0] == param[1]) ? 1 : 0;
                break;

            case OP_BASE_ADD:
                TRACE(("BASE_ADD: "FMT_S" (+"FMT_W")", soft->base, param[0]));
                soft->base += param[0];
                TRACE((" -> "FMT_S"\n", soft->base));
                break;

            default:
                return ERR_FAILURE;
        }

        TRACE(("offset="FMT_S"\n", offset));
        soft->pc += offset;

        if(soft->pc > size) {
            return ERR_FAILURE;
        }
    }
    TRACE(("suspend\n"));
    dump(mem, size);

    return error;
}


/* Return number of positions, or -1 for failure. */
static int read_software(software_t *soft, const char *filename)
{
    FILE *f;
    icsize_t pos_num = 0;
    icword_t value;
    int n;

    f = fopen(filename, "rb");
    if(!f) {
        PANIC("Could not read file");
    }

    while(1) {
        if(pos_num > (MEM_SIZE_MAX / (int) sizeof(icword_t))) {
            PANIC("Too many positions");
        }

        n = fscanf(f, FMT_W",", &value);
        if(n < 1) {
            break;
        }
        soft->mem[soft->size++] = value;
    }

    fclose(f);
    return ERR_SUCCESS;
}


#define COLOR      0
#define DIRECTION  1
#define LEFT       0
#define RIGHT      1

typedef enum {
    BLACK = 0,
    WHITE = 1,
} color_t;

#define COLOR_STR(color)  ((color) ? "WHITE" : "BLACK")

typedef struct {
    color_t color;
    int x;
    int y;
} panel_t;

#define PANEL_NUM  4096

typedef struct {
    panel_t painted[PANEL_NUM];
    unsigned num;
} surface_t;

void surface_init(surface_t *surface) {
    memset(surface, 0, sizeof(*surface));
}

panel_t *surface_find_painted_panel(surface_t *surface, int x, int y) {
    panel_t *panel;
    for(unsigned i = 0; i < surface->num; ++i) {
        panel = &surface->painted[i];
        if((panel->x == x) && (panel->y == y)) {
            return panel;
        }
    }
    return NULL;
}

color_t surface_get_panel_color(surface_t *surface, int x, int y)
{
    panel_t *panel = surface_find_painted_panel(surface, x, y);
    return panel ? panel->color : BLACK;
}

void surface_paint(surface_t *surface, color_t color, int x, int y) {
    panel_t *panel = surface_find_painted_panel(surface, x, y);

    if(panel) {
        // found a panel already painted
        TRACE(("> Paint over -> %s, x=%d, y=%d\n", COLOR_STR(color), x, y));
        panel->color = color;
    } else {
        // painted panel not found, add one
        TRACE(("> Paint empty -> %s, x=%d, y=%d\n", COLOR_STR(color), x, y));
        if(surface->num >= PANEL_NUM) {
            PANIC("Surface full");
        }
        panel = &surface->painted[surface->num++];
        panel->color = color;
        panel->x = x;
        panel->y = y;
    }
}

void surface_print(surface_t *surface)
{
    int x_min = 0, x_max = 0;
    int y_min = 0, y_max = 0;
    panel_t *panel;

    // Get painted surface size
    for(unsigned i; i < surface->num; ++i) {
        panel = &surface->painted[i];
        if(panel->x < x_min) { x_min = panel->x; }
        if(panel->x > x_max) { x_max = panel->x; }
        if(panel->y < y_min) { y_min = panel->y; }
        if(panel->y > y_max) { y_max = panel->y; }
    }

    for(int y = y_max; y >= y_min; --y) {
        for(int x = x_min; x <= x_max; ++x) {
            printf((surface_get_panel_color(surface, x, y) == WHITE) ? "#" : ".");
        }
        printf("\n");
    }
    printf("\n");
}

static surface_t ship_surface = {0};


typedef enum {
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3,
} direction_t;

typedef struct {
    software_t soft;  // keep first
    icword_t output[2];
    int output_idx;
    icword_t input;
    surface_t *surface;
    int x;
    int y;
    direction_t direction;
} painter_soft_t;

#define SOFT_TO_PAINTER(soft_ptr)  ((painter_soft_t *)(soft_ptr))
#define PAINTER_TO_SOFT(painter_ptr)  (&((painter_ptr)->soft))

static error_t painter_get_input(software_t *soft, icword_t *value)
{
    *value = SOFT_TO_PAINTER(soft)->input;
    return ERR_SUCCESS;
}

static error_t painter_set_output(software_t *soft, icword_t value)
{
    painter_soft_t *painter = SOFT_TO_PAINTER(soft);

    painter->output[painter->output_idx++] = value;

    if(painter->output_idx >= 2) {
        return ERR_YIELD_OUTPUT;
    }

    return ERR_SUCCESS;
}

// The painter output is expected to have 2 icword_t, the function panics if it
// doesn't. `buf` must point to 2 icword_t.
static void painter_read(painter_soft_t *painter, icword_t *buf)
{
    if(painter->output_idx != 2) {
        PANIC("Attempted to read incomplete buffer from painter.");
    }
    buf[0] = painter->output[0];
    buf[1] = painter->output[1];
    painter->output_idx = 0;
}

static void painter_write(painter_soft_t *painter, icword_t value)
{
    painter->input = value;
}

static void painter_init(painter_soft_t *painter, surface_t *surface)
{
    software_t *soft = PAINTER_TO_SOFT(painter);
    memset(painter, 0, sizeof(*painter));
    software_init(soft);
    soft->get_input = painter_get_input;
    soft->set_output = painter_set_output;
    painter->surface = surface;
}

static void painter_destroy(painter_soft_t *painter)
{
    software_destroy(PAINTER_TO_SOFT(painter));
}

#define PAINTER_PAINT(painter, color)  \
    surface_paint((painter)->surface, (color), (painter)->x, (painter)->y)

#define PAINTER_UPDATE_COLOR(painter)  \
    painter_write((painter), surface_get_panel_color((painter)->surface, (painter)->x, (painter)->y))

static void painter_rotate(painter_soft_t *painter, int left_right)
{
    TRACE(("> Painter rotate %s\n", (left_right == LEFT) ? "left" : "right"));
    painter->direction = (painter->direction + (left_right * 2 - 1)) % 4;
    if(painter->direction < 0) {
        painter->direction += 4;
    }
}

static void painter_move(painter_soft_t *painter) {
    switch(painter->direction) {
        case NORTH: painter->y += 1; TRACE(("> Painter move NORTH")); break;
        case EAST:  painter->x += 1; TRACE(("> Painter move EAST"));  break;
        case SOUTH: painter->y -= 1; TRACE(("> Painter move SOUTH")); break;
        case WEST:  painter->x -= 1; TRACE(("> Painter move WEST"));  break;
        default: PANIC("Invalid direction");
    }
    TRACE((" -> x=%d, y=%d\n", painter->x, painter->y));
}


static void painter_run(painter_soft_t *painter) {
    error_t error;
    icword_t painter_out[2] = {0};

    PAINTER_UPDATE_COLOR(painter);

    while(1) {
        error = run_program(PAINTER_TO_SOFT(painter));
        switch(error) {
            case ERR_SUCCESS:
                return;
            case ERR_WAIT_INPUT:
                PANIC("WAIT INPUT");
                break;
            case ERR_YIELD_OUTPUT:
                painter_read(painter, painter_out);
                PAINTER_PAINT(painter, painter_out[COLOR]);
                painter_rotate(painter, painter_out[DIRECTION]);
                painter_move(painter);
                PAINTER_UPDATE_COLOR(painter);
                break;
            case ERR_FAILURE:
            default:
                PANIC("Something went wrong");
                break;
        }
    }
}

int main(int argc, char **argv)
{
    painter_soft_t painter = {0};

    surface_init(&ship_surface);
    painter_init(&painter, &ship_surface);

    if(argc >= 2) {
        if(read_software(PAINTER_TO_SOFT(&painter), argv[1]) != ERR_SUCCESS) {
            PANIC("Error reading input");
        }
    } else {
        PANIC("Please give input file in argument 1");
    }

    surface_paint(&ship_surface, WHITE, 0, 0);
    painter_run(&painter);

    printf("Result:\n");
    surface_print(&ship_surface);

    painter_destroy(&painter);

    return 0;
}
