# ============================================================
#  intermediate_code.py  –  Generate & Display Intermediate Code
#
#  Run standalone : python assembler/intermediate_code.py
# ============================================================

import os
import data
import pass1

_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")
OUTPUT_FILE = os.path.join(_dir, "sample_IC.txt")


def display_intermediate_code():
    print("\n" + "=" * 80)
    print(f"{'INTERMEDIATE CODE':^80}")
    print("=" * 80)
    print(f"{'L#':<4} {'LABEL':<6} {'MNEMONIC':<10} {'OPERAND':<12} "
          f"{'LC':<10} {'IC1':<14} {'IC2'}")
    print("-" * 80)
    for (ln, lbl, mn, op, lc, ic1, ic2) in data.INTER:
        print(f"{ln:<4} {str(lbl or ''):<6} {str(mn or ''):<10} "
              f"{str(op  or ''):<12} {str(lc):<10} {str(ic1):<14} {str(ic2)}")
    print("=" * 80)


def write_to_file():
    with open(OUTPUT_FILE, "w") as f:
        f.write("INTERMEDIATE CODE\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'L#':<4} {'LABEL':<6} {'MNEMONIC':<10} {'OPERAND':<12} "
                f"{'LC':<10} {'IC1':<14} {'IC2'}\n")
        f.write("-" * 80 + "\n")
        for (ln, lbl, mn, op, lc, ic1, ic2) in data.INTER:
            f.write(f"{ln:<4} {str(lbl or ''):<6} {str(mn or ''):<10} "
                    f"{str(op  or ''):<12} {str(lc):<10} {str(ic1):<14} {str(ic2)}\n")
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
