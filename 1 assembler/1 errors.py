# ============================================================
#  errors.py  –  Display all Errors found during assembly
#
#  Run standalone : python assembler/errors.py
# ============================================================

import os
import data
import pass1

_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_errors():
    print("\n" + "=" * 45)
    print(f"{'ERROR REPORT':^45}")
    print("=" * 45)
    if data.ERRORS:
        for i, e in enumerate(data.ERRORS, 1):
            print(f"  {i}. [ERROR] {e}")
    else:
        print("  No errors found.")
    print("=" * 45)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_errors()
