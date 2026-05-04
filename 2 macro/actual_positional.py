# ============================================================
#  actual_positional.py  –  Actual vs Positional Parameter List (ALA)
#
#  Shows, for each macro CALL in the source, how the actual
#  arguments passed map to positional notation (#1, #2, #3 ...).
#  This is the Argument List Array (ALA) built during Pass 2.
#
#  Run standalone : python actual_positional.py  (from macro/ folder)
# ============================================================

import os
import data
import pass1
import pass2

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_actual_positional():
    print("\n" + "=" * 55)
    print(f"{'ACTUAL vs POSITIONAL PARAMETER LIST  (ALA)':^55}")
    print("=" * 55)

    if not data.ACTUAL_POSITIONAL:
        print("  (No macro calls with arguments found)")
        print("=" * 55)
        return

    for entry in data.ACTUAL_POSITIONAL:
        macro_name = entry['macro']
        params     = entry['params']

        print(f"\n  Macro Call : {macro_name}")
        print(f"  {'Actual Parameter':<22} {'Positional Parameter'}")
        print("  " + "-" * 40)

        if not params:
            print(f"  {'(no arguments)':<22} -")
        else:
            for p in params:
                print(f"  {p['actual']:<22} {p['positional']}")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    pass2.run_pass2()          # ALA is built during pass 2
    display_actual_positional()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
