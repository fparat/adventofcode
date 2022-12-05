#!/usr/bin/env python3

import os
import argparse
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

_dry_run = False


def sh(cmd):
    print(f"> {cmd}")
    if not _dry_run:
        subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("--lang", "-l", default="none")
    parser.add_argument("--dry-run", "-n", action="store_true")
    args = parser.parse_args()

    year = str(int(args.year))
    if int(year) < 2015:
        raise ValueError(f"invalid year {year}")

    day = str(int(args.day))
    if not 1 <= int(day) <= 25:
        raise ValueError(f"invalid day {day}")

    _dry_run = args.dry_run

    day_path = os.path.join(SCRIPT_DIR, year, f"day{day:>02}")
    day_relpath = os.path.relpath(day_path, SCRIPT_DIR)

    link_path = os.path.join(SCRIPT_DIR, "current")

    template_path = os.path.join(SCRIPT_DIR, "templates", args.lang)
    if args.lang == "none":
        template_path = None
    elif not os.path.isdir(template_path):
        raise ValueError(f'invalid lang {args.lang}, "templates/<lang>" must be a dir')

    sh(f"mkdir -vp {day_path}")
    sh(f"rm {link_path}")
    sh(f"ln -s {day_relpath} {link_path}")

    if template_path:
        sh(f"cp -vr {template_path}/* {day_path}/")
