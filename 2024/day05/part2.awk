BEGIN {
    FS = ",|[|]"
    part1 = 0
    part2 = 0
}

/\|/ {
    rules[NR][1] = $1
    rules[NR][2] = $2
}

/,/ {
    if (check()) {
        part1 += $((NF+1)/2)
        next;
    }

    while (!check()) {
        tmp = $pos1
        $pos1 = $pos2
        $pos2 = tmp
    }

    part2 += $((NF+1)/2)
}

END {
    print "Part 1: " part1
    print "Part 2: " part2
}

function check() {
    for (i = 1; i <= NF; i++) {
        for (r = 1; r <= length(rules); r++) {
            if (rules[r][2] != $i) {
                continue;
            }
            for (j = i + 1; j <= NF; j++) {
                if ($j == rules[r][1]) {
                    pos1 = i
                    pos2 = j
                    return ""
                }
            }
        }
    }

    return "ok"
}
