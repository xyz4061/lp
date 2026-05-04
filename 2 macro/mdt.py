# ============================================================
#  mdt.py  –  Display Macro Definition Table (MDT)
#
#  Run standalone : python macro/mdt.py
#              OR : python mdt.py   (from inside macro/ folder)
# ============================================================

import os
import data
import pass1

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_mdt():
    print("\n" + "=" * 45)
    print(f"{'MACRO DEFINITION TABLE  (MDT)':^45}")
    print("=" * 45)
    print(f"{'Index':<8} {'MDT Entry'}")
    print("-" * 45)
    for i, entry in enumerate(data.MDT, 1):
        print(f"{i:<8} {entry}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_mdt()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
