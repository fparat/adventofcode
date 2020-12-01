#!/bin/bash

set -e

num_lines=$(wc -l input | awk '{print $1}')

a_iter=$num_lines
b_iter=$num_lines
c_iter=$num_lines

for a in $(<input); do
    a_iter=$(( $a_iter - 1))
    b_iter=$a_iter
    for b in $(tail -n$a_iter input); do
        b_iter=$(( $b_iter - 1 ))

        if (( $(( $a + $b )) > 2020  )); then
            continue
        fi

        for c in $(tail -n$b_iter input); do
            c_iter=$(( $c_iter - 1 ))
            if [[ "$(( $a + $b + $c ))" == "2020" ]] ; then
                echo "Result: $(( $a * $b * $c ))"
                exit
            fi
        done
    done
done
