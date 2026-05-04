# ============================================================
#  Two-Pass Assembler (Python)
#  Generates: Symbol Table, Literal Table, Pool Table,
#             Intermediate Code
#  Displays:  Errors
# ============================================================

import re

# ─────────────────────────────────────────────
#  MACHINE OPCODE TABLE  (MOT)
#  Format: mnemonic -> (class, opcode)
# ─────────────────────────────────────────────
MOT = {
    # Imperative Statements (IS)
    "STOP":  ("IS", "00"),
    "ADD":   ("IS", "01"),
    "SUB":   ("IS", "02"),
    "MULT":  ("IS", "03"),
    "MOVER": ("IS", "04"),
    "MOVEM": ("IS", "05"),
    "COMP":  ("IS", "06"),
    "BC":    ("IS", "07"),
    "DIV":   ("IS", "08"),
    "READ":  ("IS", "09"),
    "PRINT": ("IS", "10"),
    "LOAD":  ("IS", "11"),

    # Assembler Directives (AD)
    "START":  ("AD", "01"),
    "END":    ("AD", "02"),
    "ORIGIN": ("AD", "03"),
    "EQU":    ("AD", "04"),
    "LTORG":  ("AD", "05"),

    # Declarative Statements (DL)
    "DS": ("DL", "01"),
    "DC": ("DL", "02"),

    # Register table (RG)
    "AREG": ("RG", "01"),
    "BREG": ("RG", "02"),
    "CREG": ("RG", "03"),
    "DREG": ("RG", "04"),

    # Condition Codes (CC)
    "EQ":  ("CC", "01"),
    "LT":  ("CC", "02"),
    "GT":  ("CC", "03"),
    "LE":  ("CC", "04"),
    "GE":  ("CC", "05"),
    "ANY": ("CC", "06"),
}

# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────
SYMTAB   = {}          # symbol -> address  (address=None if forward ref)
LITTAB   = []          # list of [literal, address]  address=None until assigned
POOLTAB  = []          # list of starting indices into LITTAB for each pool
errors   = []          # collected error messages
inter_code = []        # intermediate code lines


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def is_literal(token):
    """Check if token is a literal like ='5' or ='10'"""
    return token.startswith("='") and token.endswith("'")


def get_literal_index(lit):
    """Return index of literal in LITTAB, add if not present."""
    for i, entry in enumerate(LITTAB):
        if entry[0] == lit and entry[1] is None:   # unresolved in current pool
            return i
    # not found – add new entry
    LITTAB.append([lit, None])
    return len(LITTAB) - 1


def resolve_expression(expr, symtab):
    """
    Evaluate simple expressions like  A+4  or  A+2
    Returns integer value or None on failure.
    """
    expr = expr.strip()
    # simple symbol
    if expr in symtab and symtab[expr] is not None:
        return symtab[expr]
    # expression: SYM +/- number
    m = re.match(r'^(\w+)\s*([+\-])\s*(\d+)$', expr)
    if m:
        sym, op, num = m.group(1), m.group(2), int(m.group(3))
        if sym in symtab and symtab[sym] is not None:
            base = symtab[sym]
            return base + num if op == '+' else base - num
    return None


def assign_literals(lc):
    """
    Assign addresses to all unresolved literals in the current pool.
    Returns updated LC.
    """
    for entry in LITTAB:
        if entry[1] is None:
            entry[1] = lc
            lc += 1
    return lc


# ─────────────────────────────────────────────
#  TOKENISER  – parse one source line
# ─────────────────────────────────────────────
def tokenise(line):
    """
    Returns (label, mnemonic, operand) after stripping comments.
    All three may be None / empty string.
    """
    # strip inline comment
    line = re.split(r'\s*;', line)[0].rstrip()
    if not line.strip():
        return None, None, None

    parts = line.split()
    label = mnemonic = operand = None

    # If first token is NOT in MOT it is a label
    if parts[0].upper() not in MOT:
        label = parts[0]
        parts = parts[1:]

    if parts:
        mnemonic = parts[0].upper()
    if len(parts) > 1:
        operand = parts[1]          # take first operand token only

    return label, mnemonic, operand


# ─────────────────────────────────────────────
#  PASS 1
# ─────────────────────────────────────────────
def pass1(source_lines):
    global SYMTAB, LITTAB, POOLTAB, errors, inter_code

    LC = 0
    line_no = 0

    # Start a new pool
    POOLTAB.append(0)   # pool 1 starts at literal index 0

    for raw_line in source_lines:
        line_no += 1
        label, mnemonic, operand = tokenise(raw_line)

        if mnemonic is None:
            continue

        # ── START ──────────────────────────────
        if mnemonic == "START":
            if operand and operand.isdigit():
                LC = int(operand)
            else:
                errors.append(f"Line {line_no}: Invalid operand for START")
                LC = 0
            inter_code.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", f"(AD, 01)", f"(C,{LC})"))
            continue

        # ── END ────────────────────────────────
        if mnemonic == "END":
            # assign any remaining literals
            LC = assign_literals(LC)
            inter_code.append((line_no, label, mnemonic, operand,
                                "", "(AD, 02)", ""))
            break

        # ── LTORG ──────────────────────────────
        if mnemonic == "LTORG":
            inter_code.append((line_no, label, mnemonic, operand,
                                "", "(AD, 05)", ""))
            # assign addresses to current pool literals
            LC = assign_literals(LC)
            # start a new pool
            POOLTAB.append(len(LITTAB))
            continue

        # ── ORIGIN ─────────────────────────────
        if mnemonic == "ORIGIN":
            val = resolve_expression(operand, SYMTAB) if operand else None
            if val is not None:
                LC = val
            else:
                errors.append(f"Line {line_no}: Cannot resolve ORIGIN operand '{operand}'")
            inter_code.append((line_no, label, mnemonic, operand,
                                "", "(AD, 03)", ""))
            continue

        # ── EQU ────────────────────────────────
        if mnemonic == "EQU":
            if label:
                val = resolve_expression(operand, SYMTAB) if operand else None
                if label in SYMTAB and SYMTAB[label] is None:
                    SYMTAB[label] = val   # resolve forward ref
                elif label not in SYMTAB:
                    SYMTAB[label] = val
                else:
                    errors.append(f"Line {line_no}: Duplicate symbol '{label}'")
            else:
                errors.append(f"Line {line_no}: EQU without label")
            sym_idx = list(SYMTAB.keys()).index(label) + 1 if label in SYMTAB else "?"
            inter_code.append((line_no, label, mnemonic, operand,
                                "", "(AD, 04)", f"(S,{sym_idx:02d})"))
            continue

        # ── Handle label ───────────────────────
        if label:
            if label in SYMTAB:
                if SYMTAB[label] is None:
                    SYMTAB[label] = LC   # resolve forward reference
                else:
                    errors.append(f"Line {line_no}: Duplicate symbol '{label}'")
            else:
                SYMTAB[label] = LC

        # ── DS / DC ────────────────────────────
        if mnemonic in ("DS", "DC"):
            mot_class, mot_code = MOT[mnemonic]
            size = int(operand) if operand and operand.isdigit() else 1
            ic_operand = f"(C,{operand})" if operand else ""
            inter_code.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", f"({mot_class}, {mot_code})", ic_operand))
            LC += size
            continue

        # ── IS instructions ────────────────────
        if mnemonic in MOT:
            mot_class, mot_code = MOT[mnemonic]

            if operand and is_literal(operand):
                lit_idx = get_literal_index(operand)
                ic_op = f"(L,{lit_idx + 1:02d})"
            elif operand and operand in SYMTAB:
                sym_idx = list(SYMTAB.keys()).index(operand) + 1
                ic_op = f"(S,{sym_idx:02d})"
            elif operand:
                # forward reference – add to SYMTAB with None
                if operand not in SYMTAB:
                    SYMTAB[operand] = None
                sym_idx = list(SYMTAB.keys()).index(operand) + 1
                ic_op = f"(S,{sym_idx:02d})"
            else:
                ic_op = ""

            inter_code.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", f"({mot_class}, {mot_code})", ic_op))
            LC += 1
        else:
            errors.append(f"Line {line_no}: Unknown mnemonic '{mnemonic}'")
            inter_code.append((line_no, label, mnemonic, operand,
                                f"LC = {LC}", "(?? ERROR ??)", ""))
            LC += 1


# ─────────────────────────────────────────────
#  PASS 2  (resolve forward refs in SYMTAB)
# ─────────────────────────────────────────────
def pass2():
    for sym, addr in SYMTAB.items():
        if addr is None:
            errors.append(f"Undefined symbol: '{sym}'")


# ─────────────────────────────────────────────
#  DISPLAY FUNCTIONS
# ─────────────────────────────────────────────
def print_intermediate_code():
    print("\n" + "=" * 80)
    print(f"{'INTERMEDIATE CODE':^80}")
    print("=" * 80)
    hdr = f"{'L#':<4} {'LABEL':<6} {'MNEMONIC':<8} {'OPERAND':<10} {'LC':<10} {'IC1':<14} {'IC2':<10}"
    print(hdr)
    print("-" * 80)
    for entry in inter_code:
        ln, lbl, mn, op, lc, ic1, ic2 = entry
        print(f"{ln:<4} {str(lbl or ''):<6} {str(mn or ''):<8} {str(op or ''):<10} "
              f"{str(lc):<10} {str(ic1):<14} {str(ic2):<10}")


def print_symbol_table():
    print("\n" + "=" * 40)
    print(f"{'SYMBOL TABLE':^40}")
    print("=" * 40)
    print(f"{'R#':<5} {'SYMBOL':<10} {'ADDRESS':<10}")
    print("-" * 40)
    for i, (sym, addr) in enumerate(SYMTAB.items(), 1):
        addr_str = str(addr) if addr is not None else "-------"
        print(f"{i:<5} {sym:<10} {addr_str:<10}")


def print_literal_table():
    print("\n" + "=" * 40)
    print(f"{'LITERAL TABLE':^40}")
    print("=" * 40)
    print(f"{'R#':<5} {'LITERAL':<12} {'ADDRESS':<10}")
    print("-" * 40)
    for i, (lit, addr) in enumerate(LITTAB, 1):
        addr_str = str(addr) if addr is not None else "-------"
        print(f"{i:<5} {lit:<12} {addr_str:<10}")


def print_pool_table():
    print("\n" + "=" * 40)
    print(f"{'POOL TABLE':^40}")
    print("=" * 40)
    print(f"{'R#':<5} {'#P (Pool Start)':<20} {'#L (Literals in Pool)':<20}")
    print("-" * 40)
    for i, start in enumerate(POOLTAB):
        end = POOLTAB[i + 1] if i + 1 < len(POOLTAB) else len(LITTAB)
        count = end - start
        print(f"{i+1:<5} {start + 1:<20} {count:<20}")


def print_errors():
    print("\n" + "=" * 40)
    print(f"{'ERRORS':^40}")
    print("=" * 40)
    if errors:
        for e in errors:
            print(f"  [ERROR] {e}")
    else:
        print("  No errors found.")


def write_intermediate_file(filename="assembler/sample_IC.txt"):
    with open(filename, "w") as f:
        f.write("INTERMEDIATE CODE\n")
        f.write("=" * 80 + "\n")
        f.write(f"{'L#':<4} {'LABEL':<6} {'MNEMONIC':<8} {'OPERAND':<10} "
                f"{'LC':<10} {'IC1':<14} {'IC2':<10}\n")
        f.write("-" * 80 + "\n")
        for entry in inter_code:
            ln, lbl, mn, op, lc, ic1, ic2 = entry
            f.write(f"{ln:<4} {str(lbl or ''):<6} {str(mn or ''):<8} {str(op or ''):<10} "
                    f"{str(lc):<10} {str(ic1):<14} {str(ic2):<10}\n")
    print(f"\n[INFO] Intermediate code written to '{filename}'")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    source_file = "assembler/sample.asm"

    try:
        with open(source_file, "r") as f:
            source_lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Source file '{source_file}' not found.")
        return

    print(f"\n[INFO] Reading source file: {source_file}")
    print("[INFO] Running Pass 1 ...")
    pass1(source_lines)

    print("[INFO] Running Pass 2 ...")
    pass2()

    # ── Output ──
    print_intermediate_code()
    print_symbol_table()
    print_literal_table()
    print_pool_table()
    print_errors()
    write_intermediate_file()


if __name__ == "__main__":
    main()
