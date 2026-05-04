# ============================================================
#  pool_table.py  –  Generate & Display Pool Table
#
#  Run standalone : python assembler/pool_table.py
# ============================================================

import os
import data
import pass1

_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_pool_table():
    print("\n" + "=" * 45)
    print(f"{'POOL TABLE (POOLTAB)':^45}")
    print("=" * 45)
    print(f"{'R#':<5} {'#P (Start Index)':<20} {'#L (Literal Count)':<20}")
    print("-" * 45)
    for i, start in enumerate(data.POOLTAB):
        end   = data.POOLTAB[i + 1] if i + 1 < len(data.POOLTAB) else len(data.LITTAB)
        count = end - start
        print(f"{i+1:<5} {start + 1:<20} {count:<20}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_pool_table()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
