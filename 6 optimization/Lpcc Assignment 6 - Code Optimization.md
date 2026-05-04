# Assignment 6 – Code Optimization Techniques

## What is this assignment about?

This assignment applies various **code optimization techniques** on Three Address Code (TAC). Code optimization improves the quality of code — making it faster, smaller, or more efficient — without changing what the program does.

---

## Files in this assignment

| File | Purpose |
|---|---|
| `code_optimization.py` | Main file — menu to choose predefined or custom input |
| `optimization_predefined.py` | Directly runs all 6 sample inputs |
| `optimization_custom.py` | Takes custom TAC lines as input |

---

## How to Run

```
# From inside optimization/ folder

python code_optimization.py          # Menu — choose predefined or custom
python optimization_predefined.py    # Run all 6 samples directly
python optimization_custom.py        # Enter your own TAC lines
```

---

## Techniques Implemented

### 1. Constant Folding
Evaluate expressions where both operands are constants at compile time itself.

```
Before:  t1 = 3 * 4
After:   t1 = 12
```
No need to compute `3 * 4` at runtime — the result is always 12.

---

### 2. Constant Propagation
If a variable is assigned a constant value, replace all later uses of that variable with the constant.

```
Before:  x = 5
         t1 = x + y
After:   x = 5
         t1 = 5 + y
```

---

### 3. Copy Propagation
If a variable is just a copy of another variable (`y = x`), replace later uses of `y` with `x`.

```
Before:  t2 = t1
         t3 = t2 * c
After:   t3 = t1 * c
```
The copy instruction `t2 = t1` becomes unnecessary and can be removed by dead code elimination.

---

### 4. Dead Code Elimination
Remove instructions whose result is never used anywhere in the program.

```
Before:  t3 = 10 + 5    ← t3 is never used
After:   (removed)
```
Only temporary variables (t1, t2...) are eliminated. User variables (x, y, z) are kept.

---

### 5. Common Subexpression Elimination (CSE)
If the same expression is computed more than once and the operands haven't changed, reuse the earlier result instead of recomputing.

```
Before:  t1 = b * c
         t2 = a + t1
         t3 = b * c     ← same as t1
         t4 = d + t3
After:   t1 = b * c
         t2 = a + t1
         t3 = t1        ← reuse t1
         t4 = d + t3
```

---

### 6. Strength Reduction
Replace expensive operations with cheaper equivalent ones.

```
t1 = a * 1   →   t1 = a          (multiply by 1 is identity)
t2 = b * 2   →   t2 = b + b      (add is cheaper than multiply)
t3 = c + 0   →   t3 = c          (add 0 is identity)
t4 = d * 0   →   t4 = 0          (multiply by 0 is always 0)
t5 = e / 1   →   t5 = e          (divide by 1 is identity)
```

---

## How the program works

1. Each TAC line is parsed into a dictionary with fields: type, result, op1, op, op2
2. Each optimization function scans the instruction list and modifies it in place
3. A flag is returned to indicate if any change was made
4. All techniques are applied in sequence: Folding → Propagation → Copy → CSE → Strength → Dead Code
5. Before and after states are printed for comparison

---

## Sample Outputs

### Constant Folding
```
Before:  t1 = 3 * 4 / t2 = t1 + 2 / x = t2 / t3 = 10 + 5
After:   t2 = 12 + 2 / x = t2
```
`t1 = 3*4` folded to `t1 = 12`, then propagated. `t3 = 10+5` is dead (never used).

### CSE
```
Before:  t1 = b * c / t3 = b * c
After:   t3 = t1
```
Second `b * c` replaced with copy of `t1`.

### All Combined
```
Before:  t1 = 4*2, t2 = a+t1, t3 = 4*2, t4 = b+t3, t5 = t2*1, x = t5, t6 = c+0, y = t6, t7 = 10+5
After:   t2 = a+8, t5 = t2, x = t5, t6 = c, y = t6
```

---

## Viva Questions and Answers

**Q1. What is code optimization? What are its goals?**

Code optimization is the process of transforming a program to make it more efficient without changing its output or behavior. Goals are: reduce execution time (speed), reduce memory usage (space), and reduce power consumption. Optimization can be done at source level, intermediate code level, or machine code level.

---

**Q2. What is the difference between machine-dependent and machine-independent optimization?**

Machine-independent optimizations (like constant folding, dead code elimination, CSE) work on intermediate code and do not depend on the target hardware. Machine-dependent optimizations (like register allocation, instruction scheduling) depend on the specific processor architecture and are done during code generation.

---

**Q3. What is Constant Folding? Give an example.**

Constant folding evaluates expressions with constant operands at compile time instead of runtime. Example: `t1 = 3 * 4` is replaced by `t1 = 12` during compilation. This saves one multiplication instruction at runtime.

---

**Q4. What is the difference between Constant Propagation and Copy Propagation?**

Constant Propagation replaces a variable with a constant value when the variable is known to hold that constant. Example: `x = 5; t1 = x + y` → `t1 = 5 + y`.

Copy Propagation replaces a variable with another variable when one is just a copy of the other. Example: `t2 = t1; t3 = t2 * c` → `t3 = t1 * c`. The difference is that constant propagation deals with constants, copy propagation deals with variable-to-variable copies.

---

**Q5. What is Dead Code Elimination?**

Dead code is code whose result is never used in the rest of the program. Dead code elimination removes such instructions. Example: if `t3 = 10 + 5` and `t3` is never used anywhere, this instruction is removed. This reduces code size and execution time.

---

**Q6. What is Common Subexpression Elimination (CSE)?**

CSE identifies expressions that are computed more than once with the same operands and replaces the later occurrences with a reference to the earlier result. Example: if `b * c` is computed twice and `b` and `c` haven't changed in between, the second computation is replaced with a copy of the first result.

---

**Q7. What is Strength Reduction? Why is it useful?**

Strength reduction replaces a computationally expensive operation with a cheaper equivalent. Example: `x * 2` is replaced with `x + x` because addition is faster than multiplication on most processors. `x * 1` is replaced with just `x`. This reduces execution time.

---

**Q8. In what order should optimization techniques be applied?**

A good order is:
1. Constant Folding (creates constants)
2. Constant Propagation (spreads constants)
3. Copy Propagation (removes unnecessary copies)
4. CSE (eliminates repeated computations)
5. Strength Reduction (replaces expensive ops)
6. Dead Code Elimination (removes unused results)

Dead code elimination is best done last because earlier passes may create dead code.

---

**Q9. Can optimization change the output of a program?**

No. By definition, a correct optimization must preserve the semantics of the program — the output must remain the same for all inputs. If an optimization changes the program's behavior, it is incorrect.

---

**Q10. What is a basic block? How is it related to optimization?**

A basic block is a sequence of consecutive instructions with no branches in or out except at the entry and exit. Most local optimizations (like constant folding, CSE, dead code elimination) are applied within a basic block. Global optimizations work across multiple basic blocks.

---

**Q11. Why is dead code elimination applied only to temporaries in your program?**

In this implementation, only variables matching the pattern `t1`, `t2`, `t3`... (compiler-generated temporaries) are eliminated if unused. User-defined variables like `x`, `y`, `z` are kept even if they appear unused, because they might be output variables or used outside the visible code. Eliminating user variables could change program behavior.
