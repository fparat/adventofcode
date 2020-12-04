#!/usr/bin/env python3
# coding: utf-8

import re

MANDATORY_FIELDS = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
]

OPTIONAL_FIELDS = ["cid"]


def main():
    with open("input") as f:
        entries = f.read().split("\n\n")

    passports = []
    for entry in entries:
        elements = entry.replace("\n", " ").split()
        passport = {e[0]: e[1] for e in map(lambda e: e.split(":"), elements)}
        passports.append(passport)

    valid = 0
    for passport in passports:
        passport_fields = set(passport.keys()) - set(OPTIONAL_FIELDS)
        if passport_fields == set(MANDATORY_FIELDS):
            valid += 1

    print(f"Part 1: {valid} valid passports")


    valid = 0
    for passport in passports:
        fields = set(passport.keys()) - set(OPTIONAL_FIELDS)

        if fields != set(MANDATORY_FIELDS):
            continue

        for key in fields:
            try:
                ok = {
                    "byr": lambda x: 1920 <= int(x) <= 2002,
                    "iyr": lambda x: 2010 <= int(x) <= 2020,
                    "eyr": lambda x: 2020 <= int(x) <= 2030,
                    "hgt": lambda x: {
                        "cm": lambda x: 150 <= int(x) <= 193,
                        "in": lambda x: 59 <= int(x) <= 76,
                    }[x[-2:]](x[:-2]),
                    "hcl": lambda x: re.match(r"#[0-9a-f]{6}", x),
                    "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
                    "pid": lambda x: re.match(r"^[\d]{9}$", x),
                }[key](passport[key])
            except KeyError:
                ok = False

            if not ok:
                break
        else:
            valid += 1

    print(f"Part 2: {valid} valid passports")


if __name__ == "__main__":
    main()
