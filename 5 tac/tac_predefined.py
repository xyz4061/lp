import re

temp_count = 0
label_count = 0
tac_code = []

def reset():
    global temp_count, label_count, tac_code
    temp_count = 0
    label_count = 0
    tac_code = []

def new_temp():
    global temp_count
    temp_count += 1
    return "t" + str(temp_count)

def new_label():
    global label_count
    label_count += 1
    return label_count

def emit(instr):
    tac_code.append(instr)

TOKEN_SPEC = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('ID', r'[A-Za-z_]\w*'),
    ('ASSIGN', r':=|='),
    ('RELOP', r'<=|>=|<|>|==|!='),
    ('OP', r'[+\-*/]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMI', r';'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]
TOK_RE = re.compile('|'.join('(?P<%s>%s)' % (n, p) for n, p in TOKEN_SPEC))

def tokenise(text):
    tokens = []
    for m in TOK_RE.finditer(text):
        kind = m.lastgroup
        val = m.group()
        if kind == 'SKIP':
            continue
        tokens.append((kind, val))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def consume(self, kind=None, val=None):
        tok = self.peek()
        if kind and tok[0] != kind:
            raise SyntaxError("Expected " + kind + " got " + str(tok))
        if val and tok[1] != val:
            raise SyntaxError("Expected " + val + " got " + tok[1])
        self.pos += 1
        return tok

    def parse_program(self):
        while self.peek()[0] != 'EOF':
            self.parse_stmt()

    def parse_stmt(self):
        tok = self.peek()
        if tok[0] == 'ID' and tok[1].lower() == 'if':
            self.parse_if()
        elif tok[0] == 'ID':
            self.parse_assign()
        else:
            self.consume()

    def parse_if(self):
        self.consume('ID')
        self.consume('LPAREN')
        cond = self.parse_expr()
        self.consume('RPAREN')
        true_label = new_label()
        false_label = new_label()
        emit("if " + str(cond) + " goto (" + str(true_label) + ")")
        emit("goto (" + str(false_label) + ")")
        emit("(" + str(true_label) + ")")
        while self.peek()[0] != 'EOF':
            nxt = self.peek()
            if nxt[0] == 'ID' and nxt[1].lower() == 'if':
                break
            self.parse_assign()
        emit("(" + str(false_label) + ")")

    def parse_assign(self):
        lhs = self.consume('ID')[1]
        self.consume('ASSIGN')
        rhs = self.parse_expr()
        if self.peek()[0] == 'SEMI':
            self.consume('SEMI')
        emit(lhs + " = " + rhs)

    def parse_arith_expr(self):
        left = self.parse_term()
        while self.peek() == ('OP', '+') or self.peek() == ('OP', '-'):
            op = self.consume('OP')[1]
            right = self.parse_term()
            t = new_temp()
            emit(t + " = " + left + " " + op + " " + right)
            left = t
        return left

    def parse_expr(self):
        left = self.parse_arith_expr()
        if self.peek()[0] == 'RELOP':
            op = self.consume('RELOP')[1]
            right = self.parse_arith_expr()
            t = new_temp()
            emit(t + " = " + left + " " + op + " " + right)
            left = t
        return left

    def parse_term(self):
        left = self.parse_unary()
        while self.peek() == ('OP', '*') or self.peek() == ('OP', '/'):
            op = self.consume('OP')[1]
            right = self.parse_unary()
            t = new_temp()
            emit(t + " = " + left + " " + op + " " + right)
            left = t
        return left

    def parse_unary(self):
        if self.peek() == ('OP', '-'):
            self.consume('OP')
            operand = self.parse_unary()
            t = new_temp()
            emit(t + " = - " + operand)
            return t
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            return self.consume('NUMBER')[1]
        elif tok[0] == 'ID':
            if tok[1].lower() == 'if':
                raise SyntaxError("Unexpected if in expression")
            return self.consume('ID')[1]
        elif tok[0] == 'LPAREN':
            self.consume('LPAREN')
            val = self.parse_expr()
            self.consume('RPAREN')
            return val
        else:
            raise SyntaxError("Unexpected token " + str(tok))

def generate_tac(source):
    reset()
    tokens = tokenise(source)
    parser = Parser(tokens)
    try:
        parser.parse_program()
    except SyntaxError as e:
        print("Parse Error: " + str(e))

    print("\nInput : " + source)
    print("-" * 40)
    n = 1
    for instr in tac_code:
        if re.match(r'^\(\d+\)$', str(instr)):
            print(instr)
        else:
            print(str(n) + ") " + instr)
            n += 1
    print("-" * 40)


print("Three Address Code - Predefined Samples")
print("=" * 40)

print("\nSample 1: A = S - F * 100")
generate_tac("A = S - F * 100")

print("\nSample 2: a := b * -c + b * -c")
generate_tac("a := b * -c + b * -c")

print("\nSample 3: if (a < b) a = a - c;")
generate_tac("if (a < b) a = a - c;")

print("\nSample 4: if (a < b + c) a = a - c; c = b * c;")
generate_tac("if (a < b + c) a = a - c; c = b * c;")
