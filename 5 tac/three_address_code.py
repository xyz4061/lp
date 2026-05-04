# ============================================================
#  Three Address Code (TAC) Generator
#  Assignment No. 5
#
#  Handles:
#    1. Simple assignment  :  A = S - F * 100
#    2. Unary minus        :  a := b * -c + b * -c
#    3. if-statement       :  if (a < b) a = a - c;
#    4. if + multiple stmts:  if (a < b+c) a = a-c; c = b*c;
#
#  Run : python tac/three_address_code.py
# ============================================================

import re

# ── Globals ──────────────────────────────────────────────────
temp_count  = 0    # counter for temporaries  t1, t2 ...
label_count = 0    # counter for goto labels
tac_code    = []   # list of TAC instruction strings


def reset():
    global temp_count, label_count, tac_code
    temp_count  = 0
    label_count = 0
    tac_code    = []


def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"


def new_label():
    global label_count
    label_count += 1
    return label_count   # return int so we can patch later


def emit(instr):
    """Append one TAC instruction (string or tuple for labelled lines)."""
    tac_code.append(instr)


# ════════════════════════════════════════════════════════════
#  TOKENISER
# ════════════════════════════════════════════════════════════

TOKEN_SPEC = [
    ('NUMBER',  r'\d+(\.\d*)?'),
    ('ID',      r'[A-Za-z_]\w*'),
    ('ASSIGN',  r':=|='),
    ('RELOP',   r'<=|>=|<|>|==|!='),
    ('OP',      r'[+\-*/]'),
    ('LPAREN',  r'\('),
    ('RPAREN',  r'\)'),
    ('SEMI',    r';'),
    ('SKIP',    r'[ \t]+'),
    ('MISMATCH',r'.'),
]
TOK_RE = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC))


def tokenise(text):
    tokens = []
    for m in TOK_RE.finditer(text):
        kind = m.lastgroup
        val  = m.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, val))
    return tokens


# ════════════════════════════════════════════════════════════
#  RECURSIVE DESCENT PARSER  →  generates TAC
#
#  Grammar (simplified):
#    program   → stmt*
#    stmt      → if_stmt | assign_stmt
#    if_stmt   → IF LPAREN expr RPAREN stmt+
#    assign    → ID (ASSIGN | :=) expr SEMI?
#    expr      → term ((+|-) term)*
#    term      → unary ((*|/) unary)*
#    unary     → - unary | primary
#    primary   → NUMBER | ID | LPAREN expr RPAREN
# ════════════════════════════════════════════════════════════

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def consume(self, kind=None, val=None):
        tok = self.peek()
        if kind and tok[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {tok}")
        if val and tok[1] != val:
            raise SyntaxError(f"Expected '{val}', got '{tok[1]}'")
        self.pos += 1
        return tok

    # ── program ──────────────────────────────────────────────
    def parse_program(self):
        while self.peek()[0] != 'EOF':
            self.parse_stmt()

    # ── statement ────────────────────────────────────────────
    def parse_stmt(self):
        tok = self.peek()
        if tok[0] == 'ID' and tok[1].lower() == 'if':
            self.parse_if()
        elif tok[0] == 'ID':
            self.parse_assign()
        else:
            self.consume()   # skip unknown token

    # ── if statement ─────────────────────────────────────────
    def parse_if(self):
        self.consume('ID')          # consume 'if'
        self.consume('LPAREN')
        cond = self.parse_expr()    # condition expression → TAC
        self.consume('RPAREN')

        # label numbers (we'll patch them after we know positions)
        true_label  = new_label()   # label for true branch
        false_label = new_label()   # label after if block

        emit(f"if {cond} goto ({true_label})")
        emit(f"goto ({false_label})")
        emit(f"({true_label})")     # marker – printed as label line

        # parse body statements until we run out or hit another keyword
        while self.peek()[0] != 'EOF':
            nxt = self.peek()
            if nxt[0] == 'ID' and nxt[1].lower() == 'if':
                break
            self.parse_assign()

        emit(f"({false_label})")    # end label

    # ── assignment ───────────────────────────────────────────
    def parse_assign(self):
        lhs = self.consume('ID')[1]
        self.consume('ASSIGN')
        rhs = self.parse_expr()
        # optional semicolon
        if self.peek()[0] == 'SEMI':
            self.consume('SEMI')
        emit(f"{lhs} = {rhs}")

    # ── expression  (handles + and -) ────────────────────────
    def parse_expr(self):
        left = self.parse_term()
        while self.peek() == ('OP', '+') or self.peek() == ('OP', '-'):
            op   = self.consume('OP')[1]
            right = self.parse_term()
            t = new_temp()
            emit(f"{t} = {left} {op} {right}")
            left = t
        return left

    # ── term  (handles * and /) ──────────────────────────────
    def parse_term(self):
        left = self.parse_unary()
        while self.peek() == ('OP', '*') or self.peek() == ('OP', '/'):
            op    = self.consume('OP')[1]
            right = self.parse_unary()
            t = new_temp()
            emit(f"{t} = {left} {op} {right}")
            left = t
        return left

    # ── unary  (handles unary minus) ─────────────────────────
    def parse_unary(self):
        if self.peek() == ('OP', '-'):
            self.consume('OP')
            operand = self.parse_unary()
            t = new_temp()
            emit(f"{t} = - {operand}")
            return t
        return self.parse_primary()

    # ── expression  (arithmetic only: + and -) ───────────────
    def parse_arith_expr(self):
        left = self.parse_term()
        while self.peek() == ('OP', '+') or self.peek() == ('OP', '-'):
            op    = self.consume('OP')[1]
            right = self.parse_term()
            t = new_temp()
            emit(f"{t} = {left} {op} {right}")
            left = t
        return left

    # ── expression  (arithmetic + optional relop) ────────────
    def parse_expr(self):
        left = self.parse_arith_expr()
        if self.peek()[0] == 'RELOP':
            op    = self.consume('RELOP')[1]
            right = self.parse_arith_expr()   # RHS is full arith expr
            t = new_temp()
            emit(f"{t} = {left} {op} {right}")
            left = t
        return left

    # ── primary ──────────────────────────────────────────────
    def parse_primary(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            return self.consume('NUMBER')[1]
        elif tok[0] == 'ID':
            # don't consume 'if' as a primary
            if tok[1].lower() == 'if':
                raise SyntaxError("Unexpected 'if' in expression")
            return self.consume('ID')[1]
        elif tok[0] == 'LPAREN':
            self.consume('LPAREN')
            val = self.parse_expr()
            self.consume('RPAREN')
            return val
        else:
            raise SyntaxError(f"Unexpected token {tok}")


# ════════════════════════════════════════════════════════════
#  DISPLAY
# ════════════════════════════════════════════════════════════

def display_tac(title, expression):
    print(f"\n{'=' * 50}")
    print(f"  Input  : {expression}")
    print(f"{'=' * 50}")
    print(f"  Three Address Code:")
    print(f"  {'-' * 44}")

    line_no = 1
    for instr in tac_code:
        # label markers like (4) are printed without a line number
        if re.match(r'^\(\d+\)$', str(instr)):
            print(f"  {instr}")
        else:
            print(f"  {line_no}) {instr}")
            line_no += 1

    print(f"{'=' * 50}")


# ════════════════════════════════════════════════════════════
#  GENERATE TAC  –  main entry point
# ════════════════════════════════════════════════════════════

def generate_tac(source):
    reset()
    tokens = tokenise(source)
    parser = Parser(tokens)
    try:
        parser.parse_program()
    except SyntaxError as e:
        print(f"  [Parse Error] {e}")
    display_tac("", source)


# ════════════════════════════════════════════════════════════
#  MAIN  –  run all 4 sample inputs
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("   THREE ADDRESS CODE GENERATOR")
    print("   Assignment No. 5")
    print("=" * 50)

    print("\nChoose mode:")
    print("  1. Run all predefined sample inputs")
    print("  2. Enter custom expression")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        # ── Sample 1 ─────────────────────────────────────────
        print("\n>>> Sample 1: Simple arithmetic assignment")
        generate_tac("A = S - F * 100")

        # ── Sample 2 ─────────────────────────────────────────
        print("\n>>> Sample 2: Unary minus + repeated subexpression")
        generate_tac("a := b * -c + b * -c")

        # ── Sample 3 ─────────────────────────────────────────
        print("\n>>> Sample 3: if statement with simple condition")
        generate_tac("if (a < b) a = a - c;")

        # ── Sample 4 ─────────────────────────────────────────
        print("\n>>> Sample 4: if statement with complex condition + multiple body stmts")
        generate_tac("if (a < b + c) a = a - c; c = b * c;")

    elif choice == "2":
        print("\nExamples of valid input:")
        print("  A = S - F * 100")
        print("  a := b * -c + b * -c")
        print("  if (a < b) a = a - c;")
        print("  if (a < b + c) a = a - c; c = b * c;")
        expr = input("\nEnter expression: ").strip()
        if expr:
            generate_tac(expr)
        else:
            print("[ERROR] Empty input.")

    else:
        print("[ERROR] Invalid choice. Please enter 1 or 2.")
