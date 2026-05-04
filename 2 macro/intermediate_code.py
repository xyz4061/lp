# ============================================================
#  intermediate_code.py  –  Display Intermediate Code
#
#  Intermediate code = source lines with macro definitions
#  stripped out (only non-definition lines remain).
#
#  Run standalone : python macro/intermediate_code.py
#              OR : python intermediate_code.py  (from macro/ folder)
# ============================================================

import os
import data
import pass1

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")
OUTPUT_FILE = os.path.join(_dir, "intermediate_code.txt")


def display_intermediate_code():
    print("\n" + "=" * 45)
    print(f"{'INTERMEDIATE CODE':^45}")
    print("=" * 45)
    for line in data.INTERMEDIATE:
        print(f"  {line}")
    print("=" * 45)


def write_to_file():
    with open(OUTPUT_FILE, "w") as f:
        f.write("INTERMEDIATE CODE\n")
        f.write("=" * 45 + "\n")
        for line in data.INTERMEDIATE:
            f.write(f"  {line}\n")
    print(f"\n[INFO] Intermediate code saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_intermediate_code()
    write_to_file()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
