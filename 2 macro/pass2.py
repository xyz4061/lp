# ============================================================
#  pass2.py  –  Pass 2 of Macro Processor
#
#  Expands macro calls in the intermediate code using MNT + MDT.
#  Produces the final expanded code.
#
#  Run standalone : python macro/pass2.py
#              OR : python pass2.py   (from inside macro/ folder)
# ============================================================

import os
import data
import pass1

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")

EXPANDED = []   # final expanded output lines


def find_macro(name):
    for entry in data.MNT:
        if entry['name'] == name.upper():
            return entry
    return None


def expand_macro(mnt_entry, actual_args):
    """
    Walk MDT from mnt_entry['mdt_index'] and substitute actual args.
    Returns list of expanded lines (excluding MEND).
    """
    result = []
    start  = mnt_entry['mdt_index'] - 1   # 0-based
    for mdt_line in data.MDT[start:]:
        if mdt_line == "MEND":
            break
        parts     = mdt_line.split()
        new_parts = []
        for p in parts:
            if p.startswith('#'):
                try:
                    idx = int(p[1:]) - 1
                    new_parts.append(actual_args[idx] if idx < len(actual_args) else p)
                except ValueError:
                    new_parts.append(p)
            else:
                new_parts.append(p)
        result.append(" ".join(new_parts))
    return result


def run_pass2():
    global EXPANDED
    EXPANDED = []
    for line in data.INTERMEDIATE:
        tokens = line.split()
        if not tokens:
            continue
        macro_entry = find_macro(tokens[0])
        if macro_entry:
            actual_args = [a.rstrip(',') for a in tokens[1:]]

            # ── Build ALA (Actual vs Positional) ─────────
            ala_entry = {'macro': macro_entry['name'], 'params': []}
            for idx, arg in enumerate(actual_args, 1):
                ala_entry['params'].append({'actual': arg, 'positional': f'#{idx}'})
            data.ACTUAL_POSITIONAL.append(ala_entry)

            expanded = expand_macro(macro_entry, actual_args)
            EXPANDED.extend(expanded)
        else:
            EXPANDED.append(line)


def display_expanded():
    print("\n" + "=" * 45)
    print(f"{'EXPANDED CODE (Pass 2 Output)':^45}")
    print("=" * 45)
    for i, line in enumerate(EXPANDED, 1):
        print(f"  {i:<4} {line}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    pass1.run_pass1(lines)
    run_pass2()
    display_expanded()

    if data.ERRORS:
        print("\n[ERRORS]")
        for e in data.ERRORS:
            print(f"  {e}")
