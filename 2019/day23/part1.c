#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#include "intcode.h"


#define NIC_NUM     50

#define QUEUE_SIZE  32

typedef struct
{
    software_t soft;
    icword_t addr;
    bool addr_init;
    icword_t tx[QUEUE_SIZE];
    size_t txhead;
    size_t txtail;
    icword_t rx[QUEUE_SIZE];
    size_t rxhead;
    size_t rxtail;
} nic_t;

#define TO_NIC(soft_ptr) ((nic_t *) (soft_ptr))


static error_t nic_get_input(software_t *soft, icword_t *value)
{
    nic_t *nic = TO_NIC(soft);

    if (!nic->addr_init) {
        *value = nic->addr;
        nic->addr_init = true;
        return ERR_SUCCESS;
    }

    if (nic->rxhead == nic->rxtail) {
        *value = -1;
        return ERR_SUCCESS;
    }

    *value = nic->rx[nic->rxtail];
    nic->rxtail = (nic->rxtail + 1) % ARRAY_SIZE(nic->rx);

    return ERR_SUCCESS;
}


static error_t nic_set_output(struct software *soft, icword_t value)
{
    nic_t *nic = TO_NIC(soft);

    nic->tx[nic->txhead] = value;
    nic->txhead = (nic->txhead + 1) % ARRAY_SIZE(nic->tx);

    if (nic->txhead == nic->txtail) {
        PANIC("tx queue full");
    }

    return ERR_SUCCESS;
}


static nic_t *nic_new()
{
    nic_t *nic = malloc(sizeof(nic_t));
    memset(nic, 0, sizeof(*nic));
    intcode_init(&nic->soft);
    nic->soft.get_input = nic_get_input;
    nic->soft.set_output = nic_set_output;
    return nic;
}


static void nic_delete(nic_t *nic)
{
    intcode_destroy(&nic->soft);
    free(nic);
}


static size_t nic_tx_len(nic_t *nic)
{
    if (nic->txhead >= nic->txtail) {
        return nic->txhead - nic->txtail;
    } else {
        return ARRAY_SIZE(nic->tx) - (nic->txtail - nic->txhead);
    }
}


/* Pop a triplet value, values must be able to contain 3 values. */
static bool nic_pop_tx(nic_t *nic, icword_t *values)
{
    size_t len = nic_tx_len(nic);
    if (len < 3) {
        return false;
    }

    values[0] = nic->tx[nic->txtail];
    nic->txtail = (nic->txtail + 1) % ARRAY_SIZE(nic->tx);
    values[1] = nic->tx[nic->txtail];
    nic->txtail = (nic->txtail + 1) % ARRAY_SIZE(nic->tx);
    values[2] = nic->tx[nic->txtail];
    nic->txtail = (nic->txtail + 1) % ARRAY_SIZE(nic->tx);

    assert(nic_tx_len(nic) == (len - 3));

    return true;
}


/* Push X and Y values (2 values) */
static void nic_push_rx(nic_t *nic, const icword_t *values)
{
    for (size_t i = 0; i < 2; ++i) {
        nic->rx[nic->rxhead] = values[i];
        nic->rxhead = (nic->rxhead + 1) % ARRAY_SIZE(nic->rx);
        if (nic->rxhead == nic->rxtail) {
            PANIC("rx queue full");
        }
    }
}


static error_t nic_update(nic_t *nic)
{
    error_t err;

    err = intcode_step(&nic->soft);

    switch (err) {
        case ERR_SUCCESS:
            break;

        case ERR_WAIT_INPUT:
        case ERR_YIELD_OUTPUT:
        case ERR_FAILURE:
            PANIC("TODO");
            break;

        default:
            PANIC("unknown intcode error code");
    }

    return err;
}


static nic_t *nic_from_file(const char *path)
{
    nic_t *nic = nic_new();

    if(intcode_read_from_file(&nic->soft, path) != ERR_SUCCESS) {
        PANIC("Error reading input");
    }

    return nic;
}


static nic_t *nic_clone(const nic_t *src)
{
    nic_t *dst = nic_new();
    intcode_clone(&dst->soft, &src->soft);
    assert(dst->soft.mem != NULL);
    return dst;
}


int main(int argc, char **argv)
{
    nic_t *nics[50] = {0};
    nics[0] = nic_from_file(argc >= 2 ? argv[1] : "input");
    nics[0]->addr = 0;

    for (size_t i = 1; i < ARRAY_SIZE(nics); ++i) {
        nics[i] = nic_clone(nics[0]);
        nics[i]->addr = i;
    }

    while (1) {
        for (size_t i = 0; i < ARRAY_SIZE(nics); ++i) {
            nic_t *nic = nics[i];

            nic_update(nic);

            icword_t values[3] = {0};
            if (nic_pop_tx(nic, values)) {
                if (values[0] == 255) {
                    printf("Part 1: " FMT_W "\n", values[2]);
                    goto part1_end;
                }
                nic_push_rx(nics[values[0]], &values[1]);
            }
        }
    }
    part1_end:

    for (size_t i = 0; i < ARRAY_SIZE(nics); ++i) {
        nic_delete(nics[i]);
    }
    printf("done\n");
    return 0;
}
