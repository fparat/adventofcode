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
    bool rx_waiting;
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
        nic->rx_waiting = true;
        return ERR_SUCCESS;
    }

    *value = nic->rx[nic->rxtail];
    nic->rxtail = (nic->rxtail + 1) % ARRAY_SIZE(nic->rx);
    nic->rx_waiting = false;

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


/* Returns true if the nic is active (not idle) */
static void nic_update(nic_t *nic)
{
    error_t err = intcode_step(&nic->soft);
    assert(err == ERR_SUCCESS);
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


static void part1(int argc, char **argv)
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
}


static bool network_is_idle(nic_t **nics, size_t nic_num)
{
    for (size_t i = 0; i < nic_num; ++i) {
        nic_t *nic = nics[i];
        if (!nic->rx_waiting) {
            return false;
        }
        if (nic->rxhead != nic->rxtail) /* queue non empty */ {
            return false;
        }
    }

    return true;
}


static void part2(int argc, char **argv)
{
    nic_t *nics[50] = {0};
    icword_t nat[2] = {0};
    icword_t nat_last_y = -1;
    nics[0] = nic_from_file(argc >= 2 ? argv[1] : "input");
    nics[0]->addr = 0;

    for (size_t i = 1; i < ARRAY_SIZE(nics); ++i) {
        nics[i] = nic_clone(nics[0]);
        nics[i]->addr = i;
    }

    while (1) {
        for (size_t i = 0; i < ARRAY_SIZE(nics); ++i) {
            nic_t *nic = nics[i];
            icword_t values[3] = {0};

            nic_update(nic);

            if (nic_pop_tx(nic, values)) {
                if (values[0] == 255) {
                    nat[0] = values[1];
                    nat[1] = values[2];
                } else {
                    nic_push_rx(nics[values[0]], &values[1]);
                }
            }
        }

        if (network_is_idle(nics, ARRAY_SIZE(nics))) {
            nic_push_rx(nics[0], nat);
            if (nat_last_y == nat[1]) {
                printf("Part 2: " FMT_W "\n", nat[1]);
                break;
            }
            nat_last_y = nat[1];
        }
    }

    for (size_t i = 0; i < ARRAY_SIZE(nics); ++i) {
        nic_delete(nics[i]);
    }
}

int main(int argc, char **argv)
{
    part1(argc, argv);
    part2(argc, argv);
    printf("done\n");
    return 0;
}
