#include <stdio.h>
#include <stdlib.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

// DIGIT(543210, 3) -> 3
#define DIGIT(n, i)  (((i) == 0) ? ((n) % 10) : (((n) / POW10[i]) % 10))

static const int POW10[6] = { 1, 10, 100, 1000, 10000, 100000 };

static int pw_is_valid(int pw) {
    // no range check, constrained upstream

    // 2 adjacent digits are the same
    if( (DIGIT(pw, 0) != DIGIT(pw, 1))
        && (DIGIT(pw, 1) != DIGIT(pw, 2))
        && (DIGIT(pw, 2) != DIGIT(pw, 3))
        && (DIGIT(pw, 3) != DIGIT(pw, 4))
        && (DIGIT(pw, 4) != DIGIT(pw, 5))
    ) {
        return 0;
    }

    // digits increase
    return ((DIGIT(pw, 5) <= DIGIT(pw, 4))
        && (DIGIT(pw, 4) <= DIGIT(pw, 3))
        && (DIGIT(pw, 3) <= DIGIT(pw, 2))
        && (DIGIT(pw, 2) <= DIGIT(pw, 1))
        && (DIGIT(pw, 1) <= DIGIT(pw, 0))) ? 1 : 0;
}

int main() {
    int low, high;
    int pw;
    int pw_num = 0;

    FILE *f = fopen("input", "rb");
    if(fscanf(f, "%d-%d", &low, &high) != 2) {
        PANIC("Invalid input");
    }
    fclose(f);
    printf("Input: %d -> %d\n", low, high);

    for(pw = low; pw < high; ++pw) {
        pw_num += pw_is_valid(pw);
    }

    printf("Result: %d\n", pw_num);

    return 0;
}
