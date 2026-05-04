# ============================================================
#  pass1.py  –  First Pass of Two-Pass Assembler
#  Reads sample.asm and fills SYMTAB, LITTAB, POOLTAB, INTER
# ============================================================

import re
import os
import data

# Works whether you run from workspace root or from assembler/ folder
_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


# ── Helpers ──────────────────────────────────────────────────

def is_literal(token):
    return token.startswith("='") and token.endswith("'")


def get_or_add_literal(lit):
    """Return index of unresolved literal in LITTAB, add if missing."""
    for i, entry in enumerate(data.LITTAB):
        if entry[0] == lit and entry[1] is None:
            return i
    data.LITTAB.append([lit, None])
    return len(data.LITTAB) - 1


def resolve_expr(expr):
    """Evaluate expressions like A+4 or A-2 using current SYMTAB."""
    expr = expr.strip()
    if expr in data.SYMTAB and data.SYMTAB[expr] is not None:
        return data.SYMTAB[expr]
    m = re.match(r'^(\w+)\s*([+\-])\s*(\d+)$', expr)
    if m:
        sym, op, num = m.group(1), m.group(2), int(m.group(3))
        if sym in data.SYMTAB and data.SYMTAB[sym] is not None:
            base = data.SYMTAB[sym]
            return base + num if op == '+' else base - num
    return None


def tokenise(line):
    """Return (label, mnemonic, operand) after stripping comments."""
    line = re.split(r'\s*;', line)[0].rstrip()
    if not line.strip():
        return None, None, None
    parts = line.split()
    label = mnemonic = operand = None
    if parts[0].upper() not in data.MOT:
        label = parts[0]
        parts = parts[1:]
    if parts:
        mnemonic = parts[0].upper()
    if len(parts) > 1:
        operand = parts[1]
    return label, mnemonic, operand


def assign_literals(lc):
    """Assign addresses to all unresolved literals; return updated LC."""
    for entry in data.LITTAB:
        if entry[1] is None:
            entry[1] = lc
            lc += 1
    return lc


# ── Pass 1 ───────────────────────────────────────────────────

def run_pass1(source_lines):
    LC = 0
    data.POOLTAB.append(0)   # Pool 1 starts at literal index 0

    for line_no, raw in enumerate(source_lines, 1):
        label, mnemonic, operand = tokenise(raw)
        if mnemonic is None:
            continue

        # ── START ──────────────────────────────────────────
        if mnemonic == "START":
            LC = int(operand) if operand and operand.isdigit() else 0
            data.INTER.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", "(AD, 01)", f"(C,{LC})"))
            continue

        # ── END ────────────────────────────────────────────
        if mnemonic == "END":
            LC = assign_literals(LC)
            data.INTER.append((line_no, label, mnemonic, operand,
                                "", "(AD, 02)", ""))
            break

        # ── LTORG ──────────────────────────────────────────
        if mnemonic == "LTORG":
            data.INTER.append((line_no, label, mnemonic, operand,
                                "", "(AD, 05)", ""))
            LC = assign_literals(LC)
            data.POOLTAB.append(len(data.LITTAB))   # new pool starts here
            continue

        # ── ORIGIN ─────────────────────────────────────────
        if mnemonic == "ORIGIN":
            val = resolve_expr(operand) if operand else None
            if val is not None:
                LC = val
            else:
                data.ERRORS.append(
                    f"Line {line_no}: Cannot resolve ORIGIN operand '{operand}'")
            data.INTER.append((line_no, label, mnemonic, operand,
                                "", "(AD, 03)", ""))
            continue

        # ── EQU ────────────────────────────────────────────
        if mnemonic == "EQU":
            val = resolve_expr(operand) if operand else None
            if label:
                if label in data.SYMTAB:
                    if data.SYMTAB[label] is None:
                        data.SYMTAB[label] = val
                    else:
                        data.ERRORS.append(
                            f"Line {line_no}: Duplicate symbol '{label}'")
                else:
                    data.SYMTAB[label] = val
            else:
                data.ERRORS.append(f"Line {line_no}: EQU without label")
            sym_idx = (list(data.SYMTAB.keys()).index(label) + 1
                       if label and label in data.SYMTAB else "?")
            data.INTER.append((line_no, label, mnemonic, operand,
                                "", "(AD, 04)", f"(S,{sym_idx:02d})"))
            continue

        # ── Handle label ───────────────────────────────────
        if label:
            if label in data.SYMTAB:
                if data.SYMTAB[label] is None:
                    data.SYMTAB[label] = LC
                else:
                    data.ERRORS.append(
                        f"Line {line_no}: Duplicate symbol '{label}'")
            else:
                data.SYMTAB[label] = LC

        # ── DS / DC ────────────────────────────────────────
        if mnemonic in ("DS", "DC"):
            cls, code = data.MOT[mnemonic]
            size = int(operand) if operand and operand.isdigit() else 1
            data.INTER.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", f"({cls}, {code})",
                                f"(C,{operand})"))
            LC += size
            continue

        # ── IS instructions ────────────────────────────────
        if mnemonic in data.MOT:
            cls, code = data.MOT[mnemonic]
            if operand and is_literal(operand):
                idx = get_or_add_literal(operand)
                ic_op = f"(L,{idx + 1:02d})"
            elif operand:
                if operand not in data.SYMTAB:
                    data.SYMTAB[operand] = None   # forward reference
                sym_idx = list(data.SYMTAB.keys()).index(operand) + 1
                ic_op = f"(S,{sym_idx:02d})"
            else:
                ic_op = ""
            data.INTER.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", f"({cls}, {code})", ic_op))
            LC += 1

        else:
            data.ERRORS.append(
                f"Line {line_no}: Unknown mnemonic '{mnemonic}'")
            data.INTER.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", "(?? ERROR ??)", ""))
            LC += 1


# ── Run standalone ───────────────────────────────────────────

if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    run_pass1(lines)

    print("\n[Pass 1 complete]")
    print(f"  Symbols  : {len(data.SYMTAB)}")
    print(f"  Literals : {len(data.LITTAB)}")
    print(f"  Pools    : {len(data.POOLTAB)}")
    print(f"  IC lines : {len(data.INTER)}")
    if data.ERRORS:
        print("\nErrors found during Pass 1:")
        for e in data.ERRORS:
            print(f"  {e}")
