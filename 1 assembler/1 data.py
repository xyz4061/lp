# ============================================================
#  data.py  –  Shared data structures & MOT
#  All other modules import from here
# ============================================================

# ── Machine Opcode Table (MOT) ───────────────────────────────
# mnemonic -> (class, opcode)
MOT = {
    # Imperative Statements
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
    # Assembler Directives
    "START":  ("AD", "01"),
    "END":    ("AD", "02"),
    "ORIGIN": ("AD", "03"),
    "EQU":    ("AD", "04"),
    "LTORG":  ("AD", "05"),
    # Declarative Statements
    "DS": ("DL", "01"),
    "DC": ("DL", "02"),
    # Registers
    "AREG": ("RG", "01"),
    "BREG": ("RG", "02"),
    "CREG": ("RG", "03"),
    "DREG": ("RG", "04"),
    # Condition Codes
    "EQ":  ("CC", "01"),
    "LT":  ("CC", "02"),
    "GT":  ("CC", "03"),
    "LE":  ("CC", "04"),
    "GE":  ("CC", "05"),
    "ANY": ("CC", "06"),
}

# ── Shared tables (populated by pass1.py) ───────────────────
SYMTAB  = {}   # symbol -> address  (None = forward reference)
LITTAB  = []   # [ [literal, address], ... ]
POOLTAB = []   # [ start_index_in_LITTAB, ... ]
INTER   = []   # intermediate code tuples
ERRORS  = []   # error strings
