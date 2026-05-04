# ============================================================
#  literal_table.py  –  Generate & Display Literal Table
#
#  Run standalone : python assembler/literal_table.py
# ============================================================

import os
import data
import pass1

_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_literal_table():
    print("\n" + "=" * 45)
    print(f"{'LITERAL TABLE (LITTAB)':^45}")
    print("=" * 45)
    print(f"{'R#':<5} {'LITERAL':<14} {'ADDRESS':<10}")
    print("-" * 45)
    for i, (lit, addr) in enumerate(data.LITTAB, 1):
        addr_str = str(addr) if addr is not None else "-------"
        print(f"{i:<5} {lit:<14} {addr_str:<10}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_literal_table()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
