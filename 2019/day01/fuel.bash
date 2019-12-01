#!/usr/bin/env bash

let fuel=0

while read line; do
    let modfuel=line/3-2
    let fuel=fuel+modfuel
done < input

echo "fuel=$fuel"
