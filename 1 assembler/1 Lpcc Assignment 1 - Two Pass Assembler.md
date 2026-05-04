# Assignment 1 – Two Pass Assembler

## What is this assignment about?

A **Two Pass Assembler** reads assembly language source code and converts it into machine-readable intermediate code. It also builds three important tables — Symbol Table, Literal Table, and Pool Table — and detects errors in the source program.

---

## Files in this assignment

| File | Purpose |
|---|---|
| `sample.asm` | Input assembly source program |
| `data.py` | Shared data structures — MOT, SYMTAB, LITTAB, POOLTAB |
| `pass1.py` | First pass — reads source, fills all tables |
| `symbol_table.py` | Displays Symbol Table only |
| `literal_table.py` | Displays Literal Table only |
| `pool_table.py` | Displays Pool Table only |
| `intermediate_code.py` | Displays Intermediate Code only |
| `errors.py` | Displays Errors only |
| `main.py` | Runs everything together |

---

## How to Run

```
# From inside assembler/ folder

python symbol_table.py         # Symbol Table only
python literal_table.py        # Literal Table only
python pool_table.py           # Pool Table only
python intermediate_code.py    # Intermediate Code only
python errors.py               # Errors only
python main.py                 # Everything together
```

---

## How it works — Step by Step

### Pass 1
1. Read source file line by line
2. For each line — identify label, mnemonic, operand
3. Compare mnemonic with MOT (Machine Opcode Table)
4. If label found → add to SYMTAB with current LC value
5. If literal found (like `='5'`) → add to LITTAB with address = None
6. If `LTORG` found → assign addresses to all pending literals, start new pool in POOLTAB
7. If `ORIGIN` → update LC to new value
8. If `EQU` → assign value to symbol from expression
9. Generate intermediate code for each line
10. Collect errors (unknown mnemonic, duplicate symbol, etc.)

### Pass 2
- Resolve any remaining forward references in SYMTAB
- Report undefined symbols as errors

---

## Tables Explained

### MOT (Machine Opcode Table)
Hard-coded table mapping each mnemonic to its class and opcode.
- IS = Imperative Statement (actual instructions like ADD, LOAD)
- AD = Assembler Directive (START, END, ORIGIN, EQU, LTORG)
- DL = Declarative Statement (DS, DC)
- RG = Register (AREG, BREG, CREG, DREG)

### SYMTAB (Symbol Table)
Stores every label/symbol and its address.
- Forward references are stored with address = None initially
- Address is filled in when the label is actually encountered

### LITTAB (Literal Table)
Stores every literal (like `='5'`, `='10'`) and its assigned address.
- Address is None until LTORG or END is encountered

### POOLTAB (Pool Table)
Stores the starting index in LITTAB for each pool.
- A new pool starts at the beginning and after every LTORG

### Intermediate Code
One line per source instruction in the format:
```
(class, opcode)  (type, index)
```
Example: `(IS, 01)  (S, 02)` means ADD instruction with symbol at index 2

---

## Sample Program Explanation

```
        START   100       → LC starts at 100
A       DC      01        → A gets address 100, stores constant 1
        LOAD    A         → Load value at A
        LOAD    C         → Load value at C (forward reference)
        ADD     ='5'      → Add literal 5 (goes to LITTAB)
        AD      D         → ERROR: AD is not a valid mnemonic
        ORIGIN  A+2       → LC jumps to 100+2 = 102
        MULT    ='10'     → Multiply by literal 10
        ADD     L         → Add value at L (forward reference)
        LTORG             → Assign addresses to ='5' and ='10', start pool 2
L       ADD     ='5'      → L gets address 106
        ADD     B
B       DS      1         → B gets address 108, reserves 1 word
C       EQU     B         → C = address of B = 108
A       DS      1         → ERROR: A already defined
        END
```

---

## Errors in Sample Program

1. **Line 6 — Unknown mnemonic 'D'** : `AD D` — `AD` is not in MOT, so `AD` is treated as a label and `D` as the mnemonic. `D` is not valid.
2. **Line 15 — Duplicate symbol 'A'** : `A` was already defined at line 2 with address 100.

---

## Viva Questions and Answers

**Q1. What is a Two Pass Assembler? Why two passes?**

A Two Pass Assembler reads the source code twice. The first pass builds the symbol table and generates intermediate code. The second pass resolves forward references — symbols that are used before they are defined. One pass is not enough because when we encounter a forward reference, we don't know its address yet.

---

**Q2. What is a forward reference? Give an example.**

A forward reference is when a symbol is used in an instruction before it is defined (assigned an address) in the program. Example: `LOAD C` appears at line 4 but `C EQU B` is defined at line 14. During Pass 1, C is added to SYMTAB with address None and resolved later.

---

**Q3. What is the difference between SYMTAB, LITTAB, and POOLTAB?**

- SYMTAB stores user-defined labels and their addresses
- LITTAB stores literals (constant values like `='5'`) and their addresses
- POOLTAB stores the starting index in LITTAB for each pool of literals. A new pool is created at the start and after each LTORG.

---

**Q4. What is LTORG? What does it do?**

LTORG (Literal Origin) is an assembler directive that forces the assembler to assign addresses to all literals collected so far. Without LTORG, literals are assigned addresses at the END of the program. LTORG allows literals to be placed closer to where they are used.

---

**Q5. What is the purpose of the MOT?**

The Machine Opcode Table (MOT) is a hard-coded table that maps each mnemonic to its class (IS/AD/DL/RG) and opcode number. The assembler uses it to identify valid instructions and generate the correct intermediate code representation.

---

**Q6. What is intermediate code? What is its format?**

Intermediate code is a machine-independent representation of the source program generated during Pass 1. Each instruction is represented as a tuple of (class, opcode) and (type, index). For example, `LOAD A` becomes `(IS, 11) (S, 01)` where S means symbol and 01 is the index of A in SYMTAB.

---

**Q7. What is the Location Counter (LC)?**

The Location Counter keeps track of the memory address of the current instruction being processed. It starts at the value given in the START directive and increments by 1 for each instruction. DS increments it by the size specified. ORIGIN can change it to any value.

---

**Q8. What is EQU? How is it different from DS?**

EQU assigns a symbolic name to an expression or another symbol's value. It does not allocate memory. DS (Define Storage) actually reserves memory locations. Example: `C EQU B` means C has the same address as B, but no new memory is allocated.

---

**Q9. What errors does your assembler detect?**

1. Unknown mnemonic — instruction not found in MOT
2. Duplicate symbol — same label defined more than once
3. Undefined symbol — symbol used but never defined (caught in Pass 2)
4. Cannot resolve ORIGIN expression — when the symbol in ORIGIN is not yet defined

---

**Q10. What is the difference between IS, AD, DL in MOT?**

- IS (Imperative Statement) — actual executable instructions like ADD, LOAD, MULT
- AD (Assembler Directive) — instructions for the assembler itself like START, END, LTORG, ORIGIN, EQU
- DL (Declarative Statement) — data definition instructions like DS (Define Storage) and DC (Define Constant)
