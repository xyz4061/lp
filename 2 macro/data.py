# ============================================================
#  data.py  –  Shared data structures for Macro Processor
#  All other modules import from here
# ============================================================

# Macro Name Table  (MNT)
# Each entry: { 'name': str, 'num_params': int, 'mdt_index': int,
#               'formal_params': [str, ...] }
MNT = []

# Macro Definition Table  (MDT)
# Each entry: str  (one line of macro body, params replaced with #1,#2...)
MDT = []

# Intermediate Code
# Lines that are NOT macro definitions (non-MACRO/MEND lines outside defs)
INTERMEDIATE = []

# Formal vs Positional Parameter Table
# One entry per macro:
#   { 'macro': str,
#     'params': [ {'formal': str, 'positional': str}, ... ] }
FORMAL_POSITIONAL = []

# Actual vs Positional (ALA – Argument List Array)
# One entry per macro CALL in the source:
#   { 'macro': str,
#     'params': [ {'actual': str, 'positional': str}, ... ] }
ACTUAL_POSITIONAL = []

# Errors
ERRORS = []
