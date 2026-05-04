# Assignment 5 – Three Address Code (TAC) Generator

## What is this assignment about?

This assignment generates **Three Address Code (TAC)** for given expressions. TAC is an intermediate code representation where each instruction has at most one operator and at most three operands (result, op1, op2). It is used as an intermediate step between source code and machine code in a compiler.

---

## Files in this assignment

| File | Purpose |
|---|---|
| `three_address_code.py` | Main file — menu to choose predefined or custom input |
| `tac_predefined.py` | Directly runs all 4 sample inputs |
| `tac_custom.py` | Takes custom expression as input |

---

## How to Run

```
# From inside tac/ folder

python three_address_code.py    # Menu — choose predefined or custom
python tac_predefined.py        # Run all 4 samples directly
python tac_custom.py            # Enter your own expression
```

---

## How it works — Step by Step

1. **Tokeniser** — breaks the input expression into tokens (ID, NUMBER, OP, RELOP, ASSIGN, etc.) using regex
2. **Recursive Descent Parser** — parses tokens according to grammar rules
3. **TAC Generation** — every binary/unary operation creates a new temporary variable and emits one TAC instruction
4. **Output** — numbered TAC instructions with label markers for if-statements

### Grammar used
```
program  → stmt*
stmt     → if_stmt | assign_stmt
if_stmt  → if ( expr ) stmt+
assign   → ID = expr ;
expr     → arith_expr (relop arith_expr)?
arith_expr → term ((+ | -) term)*
term     → unary ((* | /) unary)*
unary    → - unary | primary
primary  → NUMBER | ID | ( expr )
```

---

## Sample Inputs and Outputs

### Sample 1 — Simple arithmetic
```
Input  : A = S - F * 100
Output :
  1) t1 = F * 100
  2) t2 = S - t1
  3) A = t2
```
Operator precedence is respected — `*` before `-`.

### Sample 2 — Unary minus
```
Input  : a := b * -c + b * -c
Output :
  1) t1 = - c
  2) t2 = b * t1
  3) t3 = - c
  4) t4 = b * t3
  5) t5 = t2 + t4
  6) a = t5
```
Each unary minus creates a separate temporary.

### Sample 3 — if statement
```
Input  : if (a < b) a = a - c;
Output :
  1) t1 = a < b
  2) if t1 goto (1)
  3) goto (2)
  (1)
  4) t2 = a - c
  5) a = t2
  (2)
```

### Sample 4 — if with complex condition
```
Input  : if (a < b + c) a = a - c; c = b * c;
Output :
  1) t1 = b + c
  2) t2 = a < t1
  3) if t2 goto (1)
  4) goto (2)
  (1)
  5) t3 = a - c
  6) a = t3
  7) t4 = b * c
  8) c = t4
  (2)
```

---

## Viva Questions and Answers

**Q1. What is Three Address Code?**

Three Address Code is an intermediate representation of a program where each instruction contains at most one operator and at most three addresses (one result and up to two operands). The general form is `result = op1 operator op2`. It is called "three address" because each instruction references at most three memory locations or variables.

---

**Q2. Why do we use intermediate code like TAC?**

Intermediate code makes the compiler machine-independent. The front end (lexer + parser) generates TAC, and the back end converts TAC to machine code for a specific architecture. This separation means the same front end can target multiple machines, and optimizations can be applied on TAC before generating machine code.

---

**Q3. What is a temporary variable in TAC?**

A temporary variable (t1, t2, t3...) is a compiler-generated variable used to hold intermediate results of sub-expressions. For example, in `A = S - F * 100`, the result of `F * 100` is stored in `t1` before being used in the subtraction.

---

**Q4. How is operator precedence handled in your TAC generator?**

Operator precedence is handled naturally by the recursive descent parser structure. The grammar has separate rules for `expr` (handles + and -), `term` (handles * and /), and `unary` (handles unary minus). Since `term` is called inside `expr`, multiplication and division are always evaluated before addition and subtraction.

---

**Q5. What is a recursive descent parser?**

A recursive descent parser is a top-down parser where each grammar rule is implemented as a function. The parser starts from the top-level rule and recursively calls functions for sub-rules. It is easy to implement manually and works well for simple grammars without left recursion.

---

**Q6. How is an if-statement represented in TAC?**

An if-statement is converted into:
1. TAC for the condition expression → result in a temporary
2. `if temp goto (true_label)` — jump to true branch if condition holds
3. `goto (false_label)` — otherwise skip the body
4. Label marker for true branch
5. TAC for body statements
6. Label marker for end (false label)

---

**Q7. What is the difference between `=` and `:=` in your program?**

Both are treated as assignment operators. `:=` is the Pascal-style assignment and `=` is the C-style assignment. The tokeniser recognises both as the ASSIGN token, so both work the same way in the parser.

---

**Q8. What is a relational operator? How is it handled?**

A relational operator compares two values and produces a boolean result. Examples: `<`, `>`, `<=`, `>=`, `==`, `!=`. In TAC, a relational expression like `a < b` is converted to `t1 = a < b`. The result `t1` is then used in the `if t1 goto` instruction.

---

**Q9. What are the types of TAC instructions?**

1. Binary assignment: `t1 = a + b`
2. Unary assignment: `t1 = - a`
3. Copy: `a = t1`
4. Conditional jump: `if t1 goto (L)`
5. Unconditional jump: `goto (L)`
6. Label: `(L)`

---

**Q10. What is the role of the tokeniser in your program?**

The tokeniser (lexer) takes the raw input string and breaks it into a list of tokens. Each token has a type (like ID, NUMBER, OP, RELOP) and a value. The parser then works on this token list instead of raw characters. This separation makes the parser simpler and cleaner.
