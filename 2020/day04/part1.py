#!/usr/bin/env python3
# coding: utf-8


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


if __name__ == "__main__":
    main()
