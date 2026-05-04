# ============================================================
#  main.py  –  Run the complete Macro Processor
#              Displays MNT, MDT, Intermediate Code,
#              Expanded Code, and any Errors
#
#  Run : python macro/main.py
#    OR : python main.py   (from inside macro/ folder)
# ============================================================

import os
import data
import pass1
import pass2
from mnt               import display_mnt
from mdt               import display_mdt
from intermediate_code import display_intermediate_code, write_to_file
from formal_positional import display_formal_positional
from actual_positional import display_actual_positional

_dir        = os.path.dirname(os.path.abspath(__file__))
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


def main():
    print("=" * 60)
    print(f"{'MACRO PROCESSOR  (Two-Pass)':^60}")
    print("=" * 60)

    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Source file '{SOURCE_FILE}' not found.")
        return

    print(f"\n[INFO] Source file : {SOURCE_FILE}")

    # ── Pass 1 ───────────────────────────────────────────────
    print("[INFO] Running Pass 1  (build MNT + MDT) ...")
    pass1.run_pass1(lines)
    print(f"       Macros found : {len(data.MNT)}")
    print(f"       MDT entries  : {len(data.MDT)}")

    # ── Pass 2 ───────────────────────────────────────────────
    print("[INFO] Running Pass 2  (expand macro calls) ...")
    pass2.run_pass2()
    print(f"       Expanded lines: {len(pass2.EXPANDED)}\n")

    # ── Display all outputs ──────────────────────────────────
    display_mnt()
    display_mdt()
    display_intermediate_code()
    display_formal_positional()
    display_actual_positional()
    pass2.display_expanded()
    display_errors()

    # ── Save IC to file ──────────────────────────────────────
    write_to_file()


if __name__ == "__main__":
    main()
