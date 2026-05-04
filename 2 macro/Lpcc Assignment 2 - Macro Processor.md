# Assignment 2 – Macro Processor (Two Pass)

## What is this assignment about?

A **Macro Processor** allows programmers to define macros — named blocks of code with parameters — and then expand them wherever they are called. This assignment implements a two-pass macro processor that builds MNT, MDT, and generates intermediate code, along with formal vs positional and actual vs positional parameter tables.

---

## Files in this assignment

| File | Purpose |
|---|---|
| `sample.asm` | Input source program with macro definitions and calls |
| `data.py` | Shared tables — MNT, MDT, INTERMEDIATE, FORMAL_POSITIONAL, ACTUAL_POSITIONAL |
| `pass1.py` | Pass 1 — reads source, builds MNT and MDT, extracts intermediate code |
| `pass2.py` | Pass 2 — expands macro calls using MNT and MDT |
| `mnt.py` | Displays MNT only |
| `mdt.py` | Displays MDT only |
| `intermediate_code.py` | Displays Intermediate Code only |
| `formal_positional.py` | Displays Formal vs Positional parameter table |
| `actual_positional.py` | Displays Actual vs Positional parameter table (ALA) |
| `main.py` | Runs everything together |

---

## How to Run

```
# From inside macro/ folder

python mnt.py                  # MNT only
python mdt.py                  # MDT only
python intermediate_code.py    # Intermediate Code only
python formal_positional.py    # Formal vs Positional table
python actual_positional.py    # Actual vs Positional (ALA) table
python pass2.py                # Expanded code only
python main.py                 # Everything together
```

---

## How it works — Step by Step

### Pass 1
1. Read source line by line
2. When `MACRO` keyword is found — read macro name and formal parameters
3. Add entry to MNT (name, number of params, starting index in MDT)
4. Read body lines until `MEND`
5. Replace formal parameters with positional notation (#1, #2, #3...)
6. If a nested macro call is found inside the body — expand it early (early expansion)
7. Store body lines in MDT
8. Lines outside macro definitions go to INTERMEDIATE code
9. Build FORMAL_POSITIONAL table during this pass

### Pass 2
1. Read intermediate code line by line
2. For each line — check if it is a macro call (name found in MNT)
3. If yes — look up MDT, substitute actual arguments for #1, #2, #3...
4. Build ACTUAL_POSITIONAL (ALA) table during this pass
5. Output expanded code

---

## Tables Explained

### MNT (Macro Name Table)
Stores information about each macro definition.
- Macro name
- Number of parameters
- Starting index in MDT

### MDT (Macro Definition Table)
Stores the body of each macro with formal parameters replaced by positional notation.
- `STORE ARG` becomes `STORE #1`
- `STORE A2` becomes `STORE #2`
- Nested macro calls are expanded early — their expanded lines are stored directly

### Intermediate Code
Source lines with macro definitions removed. Only non-definition lines remain:
```
LOAD A
STORE B
ABC
ADD5 D1, D2, D3
END
```

### Formal vs Positional Table
Shows how formal parameter names in the macro definition map to positional slots.
```
ADD5 :  A1 → #1,  A2 → #2,  A3 → #3
```

### Actual vs Positional Table (ALA — Argument List Array)
Shows what actual arguments were passed at each macro call site.
```
ADD5 D1, D2, D3 :  D1 → #1,  D2 → #2,  D3 → #3
```

---

## Sample Program Explanation

```
MACRO ABC              → defines macro ABC with 0 parameters
    LOAD p
    SUB q
MEND

MACRO ADD1 ARG         → defines macro ADD1 with 1 parameter (ARG)
    LOAD X
    STORE ARG          → stored as STORE #1 in MDT
MEND

MACRO ADD5 A1, A2, A3  → defines macro ADD5 with 3 parameters
    STORE A2           → stored as STORE #2
    ADD1 5             → nested call, expanded early → LOAD X, STORE 5
    ADD1 10            → nested call, expanded early → LOAD X, STORE 10
    LOAD A1            → stored as LOAD #1
    LOAD A3            → stored as LOAD #3
MEND

ABC                    → macro call, no arguments
ADD5 D1, D2, D3        → macro call, D1=#1, D2=#2, D3=#3
END
```

---

## MDT Contents Explained

| Index | Entry | Explanation |
|---|---|---|
| 1 | LOAD p | Body of ABC |
| 2 | SUB q | Body of ABC |
| 3 | MEND | End of ABC |
| 4 | LOAD X | Body of ADD1 |
| 5 | STORE #1 | ARG replaced with #1 |
| 6 | MEND | End of ADD1 |
| 7 | STORE #2 | A2 replaced with #2 |
| 8 | LOAD X | Early expansion of ADD1 5 |
| 9 | STORE 5 | Early expansion of ADD1 5 |
| 10 | LOAD X | Early expansion of ADD1 10 |
| 11 | STORE 10 | Early expansion of ADD1 10 |
| 12 | LOAD #1 | A1 replaced with #1 |
| 13 | LOAD #3 | A3 replaced with #3 |
| 14 | MEND | End of ADD5 |

---

## Viva Questions and Answers

**Q1. What is a Macro? How is it different from a subroutine?**

A macro is a named block of code that is textually substituted (expanded) wherever it is called. A subroutine is a separate block of code that is called at runtime using a CALL instruction and returns using RETURN. Macros expand at assembly time (no runtime overhead), subroutines execute at runtime (have call/return overhead but save memory since code is not duplicated).

---

**Q2. What is MNT? What does it store?**

MNT stands for Macro Name Table. It stores the name of each macro, the number of parameters it takes, and the starting index in the MDT where its body begins. It is used during Pass 2 to locate the macro body for expansion.

---

**Q3. What is MDT? How are parameters stored in it?**

MDT stands for Macro Definition Table. It stores the body of each macro. Formal parameter names are replaced with positional notation — the first parameter becomes #1, second becomes #2, and so on. This makes substitution easy during expansion.

---

**Q4. What is the difference between formal and actual parameters?**

Formal parameters are the names used in the macro definition (like A1, A2, A3 in `MACRO ADD5 A1, A2, A3`). Actual parameters are the values passed when the macro is called (like D1, D2, D3 in `ADD5 D1, D2, D3`). During expansion, each formal parameter is replaced by the corresponding actual parameter.

---

**Q5. What is ALA (Argument List Array)?**

ALA stands for Argument List Array. It is built during Pass 2 when a macro call is encountered. It maps each actual argument to its positional slot (#1, #2, #3...). This mapping is used to substitute actual values into the MDT body during expansion.

---

**Q6. What is early expansion of nested macros?**

When a macro body contains a call to another macro (nested call), the nested call is expanded immediately during Pass 1 itself. The expanded lines are stored directly in the MDT instead of the nested call. This is called early expansion. Example: `ADD1 5` inside ADD5's body is expanded to `LOAD X` and `STORE 5` in the MDT.

---

**Q7. What is intermediate code in a macro processor?**

Intermediate code is the source program with all macro definitions removed. It contains only the non-definition lines — regular instructions and macro calls. This is the input to Pass 2 for expansion.

---

**Q8. What does Pass 1 do in a macro processor?**

Pass 1 scans the source code, identifies macro definitions (MACRO...MEND blocks), builds the MNT and MDT, replaces formal parameters with positional notation, handles nested macro calls by early expansion, and produces intermediate code (source without definitions).

---

**Q9. What does Pass 2 do in a macro processor?**

Pass 2 reads the intermediate code, identifies macro calls by looking up the MNT, retrieves the macro body from MDT, substitutes actual arguments for positional parameters (#1, #2...), and produces the final expanded code.

---

**Q10. What is positional parameter passing?**

In positional parameter passing, arguments are matched to parameters based on their position. The first actual argument replaces #1, the second replaces #2, and so on. There is no keyword matching — order matters.
