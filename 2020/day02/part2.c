
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PANIC(msg)  do{ printf(msg "\n"); exit(1); }while(0)

#define PASSWORD_BUF_SIZE  32
#define PASSWORD_MAX_SIZE  31

#define MAX_ENTRIES  1024

#define STR_(s)  #s
#define STR(s)  STR_(s)


typedef struct {
    int low;
    int high;
    char letter;
    char password[PASSWORD_BUF_SIZE];
} entry_t;


int main(int argc, char **argv)
{
    const char *filename;
    if(argc >= 2) {
        filename = argv[1];
    } else {
        PANIC("Please give input file in argument 1");
    }

    FILE *f;
    int n;

    f = fopen(filename, "rb");
    if(!f) {
        PANIC("Could not read file");
    }

    entry_t entries[MAX_ENTRIES] = {0};
    int valid = 0;
    int valid2 = 0;

    while(1) {
        entry_t entry = {0};
        int n = fscanf(f, "%d-%d %c: %" STR(PASSWORD_MAX_SIZE) "s",
            &entry.low, &entry.high, &entry.letter, entry.password);
        if(n != 4) {
            break;
        }

        // Part 1 validation
        int count = 0;
        const char *password = entry.password;
        while(*password) {
            count += (*password++ == entry.letter);
        }
        valid += (count >= entry.low && count <= entry.high);

        // Part 2 validation
        int match1 = (entry.password[entry.low - 1] == entry.letter);
        int match2 = (entry.password[entry.high - 1] == entry.letter);
        valid2 += ((match1 + match2) == 1);
    }

    printf("Valid (part 1): %d\n", valid);
    printf("Valid (part 2): %d\n", valid2);

    fclose(f);


    printf("done\n");
    return 0;
}
