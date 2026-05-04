# ============================================================
#  mnt.py  –  Display Macro Name Table (MNT)
#
#  Run standalone : python macro/mnt.py
#              OR : python mnt.py   (from inside macro/ folder)
# ============================================================

import os
import data
import pass1

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_mnt():
    print("\n" + "=" * 50)
    print(f"{'MACRO NAME TABLE  (MNT)':^50}")
    print("=" * 50)
    print(f"{'R#':<5} {'Macro Name':<15} {'No. of Params':<16} {'MDT Start Index'}")
    print("-" * 50)
    for i, entry in enumerate(data.MNT, 1):
        print(f"{i:<5} {entry['name']:<15} {entry['num_params']:<16} {entry['mdt_index']}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_mnt()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
