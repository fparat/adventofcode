BEGIN {
    FS = ",|[|]"
    part1 = 0
}

/\|/ {
    rules[NR][1] = $1
    rules[NR][2] = $2
}

/,/ {
    for (i = 1; i <= NF; i++) {
        for (r = 1; r <= length(rules); r++) {
            if (rules[r][2] != $i) {
                continue;
            }
            for (j = i + 1; j <= NF; j++) {
                if ($j == rules[r][1]) {
                    next;
                }
            }
        }
    }

    part1 += $((NF+1)/2)
}

END { print "Part 1: " part1 }
