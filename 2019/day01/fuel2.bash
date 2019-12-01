#!/usr/bin/env bash

let fuel=0

while read line; do
    let modfuel=line/3-2
    let addfuel=modfuel/3-2
    while (( $addfuel >= 0 )); do
        let modfuel=modfuel+addfuel
        let addfuel=addfuel/3-2
    done
    let fuel=fuel+modfuel
done < input

echo "fuel="
echo $fuel
