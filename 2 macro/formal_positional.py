# ============================================================
#  formal_positional.py  –  Formal vs Positional Parameter List
#
#  Shows, for each macro definition, how formal parameter names
#  map to positional notation (#1, #2, #3 ...).
#  This table is built during Pass 1.
#
#  Run standalone : python formal_positional.py  (from macro/ folder)
# ============================================================

import os
import data
import pass1

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def display_formal_positional():
    print("\n" + "=" * 55)
    print(f"{'FORMAL vs POSITIONAL PARAMETER LIST':^55}")
    print("=" * 55)

    if not data.FORMAL_POSITIONAL:
        print("  (No macros with parameters found)")
        print("=" * 55)
        return

    for entry in data.FORMAL_POSITIONAL:
        macro_name = entry['macro']
        params     = entry['params']

        print(f"\n  Macro : {macro_name}")
        print(f"  {'Formal Parameter':<22} {'Positional Parameter'}")
        print("  " + "-" * 40)

        if not params:
            print(f"  {'(no parameters)':<22} -")
        else:
            for p in params:
                print(f"  {p['formal']:<22} {p['positional']}")

    print("\n" + "=" * 55)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    display_formal_positional()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
