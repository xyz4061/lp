# ============================================================
#  main.py  –  Run the complete Two-Pass Assembler
#              Displays all tables + errors + saves IC file
#
#  Run : python assembler/main.py
# ============================================================

import os
import data
import pass1
from symbol_table      import display_symbol_table
from literal_table     import display_literal_table
from pool_table        import display_pool_table
from intermediate_code import display_intermediate_code, write_to_file
from errors            import display_errors

_dir = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def main():
    print("=" * 60)
    print(f"{'TWO-PASS ASSEMBLER':^60}")
    print("=" * 60)

    # ── Load source ──────────────────────────────────────────
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Source file '{SOURCE_FILE}' not found.")
        return

    print(f"\n[INFO] Source file : {SOURCE_FILE}")

    # ── Pass 1 ───────────────────────────────────────────────
    print("[INFO] Running Pass 1 ...")
    pass1.run_pass1(lines)
    print("[INFO] Pass 1 complete.\n")

    # ── Display all outputs ──────────────────────────────────
    display_intermediate_code()
    display_symbol_table()
    display_literal_table()
    display_pool_table()
    display_errors()

    # ── Save IC to file ──────────────────────────────────────
    write_to_file()


if __name__ == "__main__":
    main()


























# explain:
# Alright — I’ll help you **explain this like a pro in front of an external examiner** and also prepare you for **all possible viva questions**.

# ---

# # 🧠 1. What this program does (Start with this in viva)

# 👉 Say this first:

# > “This program is the driver code for a **Two-Pass Assembler**.
# > It reads an assembly language program, processes it in two passes, and generates:

# * Intermediate Code
# * Symbol Table
# * Literal Table
# * Pool Table
# * Error Report”

# ---

# # ⚙️ 2. Explain Code Step-by-Step (Very Important)

# ### 🔹 Imports

# ```python
# import os
# import data
# import pass1
# from symbol_table import display_symbol_table
# from literal_table import display_literal_table
# from pool_table import display_pool_table
# from intermediate_code import display_intermediate_code, write_to_file
# from errors import display_errors
# ```

# 👉 Say:

# > “Here we are importing all required modules.
# > `pass1` performs the first pass of assembler, and other modules are used to display different tables like symbol, literal, pool, and errors.”

# ---

# ### 🔹 File Path Setup

# ```python
# _dir = os.path.dirname(os.path.abspath(__file__))
# SOURCE_FILE = os.path.join(_dir, "sample.asm")
# ```

# 👉 Explain like this:

# > “This code dynamically finds the directory of the current file using `__file__`.
# > Then it constructs the path of the input assembly file (`sample.asm`).
# > This ensures portability — the program works regardless of where it is placed.”

# ⚠️ Add (very important):

# > “Instead of this, we can also give a custom path to any `.asm` file.”

# ---

# ### 🔹 Main Function Start

# ```python
# def main():
#     print("=" * 60)
#     print(f"{'TWO-PASS ASSEMBLER':^60}")
#     print("=" * 60)
# ```

# 👉 Say:

# > “This prints a formatted heading for better readability of output.”

# ---

# ### 🔹 File Reading

# ```python
# try:
#     with open(SOURCE_FILE) as f:
#         lines = f.readlines()
# except FileNotFoundError:
#     print(f"[ERROR] Source file '{SOURCE_FILE}' not found.")
#     return
# ```

# 👉 Explain:

# > “This block reads the assembly file line by line.
# > If the file is not found, it handles the error gracefully using exception handling.”

# ---

# ### 🔹 Info Display

# ```python
# print(f"\n[INFO] Source file : {SOURCE_FILE}")
# ```

# 👉 Say:

# > “This shows which input file is being processed.”

# ---

# ### 🔹 Pass 1 Execution

# ```python
# print("[INFO] Running Pass 1 ...")
# pass1.run_pass1(lines)
# print("[INFO] Pass 1 complete.\n")
# ```

# 👉 Very important explanation:

# > “Pass 1 scans the entire program and builds:

# * Symbol Table
# * Literal Table
# * Pool Table
# * Intermediate Code

# It does not generate final machine code, only prepares data for Pass 2.”

# ---

# ### 🔹 Display Outputs

# ```python
# display_intermediate_code()
# display_symbol_table()
# display_literal_table()
# display_pool_table()
# display_errors()
# ```

# 👉 Say:

# > “After Pass 1, all generated tables and intermediate code are displayed for analysis.”

# ---

# ### 🔹 Save IC File

# ```python
# write_to_file()
# ```

# 👉 Say:

# > “This function saves the intermediate code into a file for further processing in Pass 2.”

# ---

# ### 🔹 Entry Point

# ```python
# if __name__ == "__main__":
#     main()
# ```

# 👉 Say:

# > “This ensures the program runs only when executed directly, not when imported as a module.”

# ---

# # 🔥 3. Most Important Concept (External WILL ASK)

# ## 💡 What is Two-Pass Assembler?

# 👉 Say confidently:

# > “A Two-Pass Assembler processes the source code in two phases:

# * **Pass 1**: Builds symbol and literal tables, assigns addresses
# * **Pass 2**: Uses these tables to generate final machine code”

# ---

# # ❓ 4. MOST ASKED VIVA QUESTIONS (with answers)

# ## 🔹 Q1: Why do we use two passes?

# 👉

# > “Because symbols and labels may be used before they are defined.
# > Pass 1 collects all definitions, Pass 2 resolves them.”

# ---

# ## 🔹 Q2: What is Symbol Table?

# 👉

# > “It stores labels with their addresses.”

# ---

# ## 🔹 Q3: What is Literal Table?

# 👉

# > “It stores constant values used in the program, like =‘5’.”

# ---

# ## 🔹 Q4: What is Pool Table?

# 👉

# > “It keeps track of literal groups for memory allocation.”

# ---

# ## 🔹 Q5: What is Intermediate Code?

# 👉

# > “It is a structured representation of the program used for generating machine code.”

# ---

# ## 🔹 Q6: What happens in Pass 1?

# 👉

# > “Assigns addresses, builds tables, generates intermediate code.”

# ---

# ## 🔹 Q7: Why exception handling is used?

# 👉

# > “To prevent program crash if file is missing.”

# ---

# ## 🔹 Q8: Why use `os.path.join()`?

# 👉

# > “For platform-independent file path creation.”

# ---

# ## 🔹 Q9: What if `.asm` file is wrong?

# 👉

# > “Errors will be detected and displayed using the error module.”

# ---

# ## 🔹 Q10: Can this work with `.py` file?

# 👉

# > ❌
# > “No, assembler only accepts assembly language input.”

# ---

# # 🧑‍🏫 5. How to Explain in 30 Seconds (Perfect Answer)

# Say this:

# > “This is the main driver program of a Two-Pass Assembler.
# > It reads an assembly file, executes Pass 1 to generate symbol, literal, and pool tables along with intermediate code.
# > Then it displays all outputs and saves intermediate code for Pass 2 processing.
# > It also handles file errors and ensures modular design using separate components.”

# ---

# # 🎯 6. Bonus Tips (Impress External)

# * Say **“modular design”**
# * Say **“separation of concerns”**
# * Say **“pass1 handles analysis, pass2 handles synthesis”**
# * Mention **error handling**

# ---

# If you want next level prep, I can:
# ✅ Explain Pass 1 internally (line by line)
# ✅ Give viva answers for your full assembler assignment
# ✅ Simulate viva questions like examiner

# Just tell 👍

