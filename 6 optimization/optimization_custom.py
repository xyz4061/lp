import re

def is_num(s):
    try:
        float(s)
        return True
    except:
        return False

def parse_line(line):
    d = {}
    d['raw'] = line
    d['active'] = True

    if line.startswith('if ') or line.startswith('goto'):
        d['type'] = 'jump'
        return d

    if line.startswith('(') and line.endswith(')'):
        d['type'] = 'label'
        return d

    if '=' in line:
        parts = line.split('=', 1)
        d['result'] = parts[0].strip()
        rhs = parts[1].strip()
        tokens = rhs.split()

        if len(tokens) == 1:
            d['type'] = 'copy'
            d['op1'] = tokens[0]
        elif len(tokens) == 2 and tokens[0] == '-':
            d['type'] = 'unary'
            d['op'] = '-'
            d['op1'] = tokens[1]
        elif len(tokens) == 3:
            d['type'] = 'binary'
            d['op1'] = tokens[0]
            d['op'] = tokens[1]
            d['op2'] = tokens[2]
        else:
            d['type'] = 'other'

    return d

def instr_to_str(d):
    if not d['active']:
        return None
    if d['type'] in ('jump', 'label', 'other'):
        return d['raw']
    if d['type'] == 'copy':
        return d['result'] + " = " + d['op1']
    if d['type'] == 'unary':
        return d['result'] + " = - " + d['op1']
    if d['type'] == 'binary':
        return d['result'] + " = " + d['op1'] + " " + d['op'] + " " + d['op2']
    return d['raw']

def print_code(instrs, msg):
    print("\n" + msg)
    print("-" * 40)
    n = 1
    for d in instrs:
        if not d['active']:
            continue
        s = instr_to_str(d)
        if d['type'] == 'label':
            print(s)
        else:
            print(str(n) + ") " + s)
            n += 1
    print("-" * 40)

def constant_folding(instrs):
    flag = False
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] == 'binary':
            if is_num(d['op1']) and is_num(d['op2']):
                a = float(d['op1'])
                b = float(d['op2'])
                if d['op'] == '+':
                    res = a + b
                elif d['op'] == '-':
                    res = a - b
                elif d['op'] == '*':
                    res = a * b
                elif d['op'] == '/':
                    if b != 0:
                        res = a / b
                    else:
                        continue
                if res == int(res):
                    res = int(res)
                d['op1'] = str(res)
                d['type'] = 'copy'
                d.pop('op', None)
                d.pop('op2', None)
                flag = True
    return instrs, flag

def constant_propagation(instrs):
    flag = False
    known = {}
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] in ('jump', 'label'):
            continue
        if 'op1' in d and d['op1'] in known:
            d['op1'] = known[d['op1']]
            flag = True
        if 'op2' in d and d['op2'] in known:
            d['op2'] = known[d['op2']]
            flag = True
        if 'result' in d:
            if d['type'] == 'copy' and is_num(d['op1']):
                known[d['result']] = d['op1']
            else:
                if d['result'] in known:
                    del known[d['result']]
    return instrs, flag

def copy_propagation(instrs):
    flag = False
    copies = {}
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] in ('jump', 'label'):
            continue
        if 'op1' in d and d['op1'] in copies:
            d['op1'] = copies[d['op1']]
            flag = True
        if 'op2' in d and d['op2'] in copies:
            d['op2'] = copies[d['op2']]
            flag = True
        if 'result' in d:
            if d['type'] == 'copy' and not is_num(d['op1']):
                copies[d['result']] = d['op1']
            else:
                if d['result'] in copies:
                    del copies[d['result']]
            remove = [k for k, v in copies.items() if v == d['result']]
            for k in remove:
                del copies[k]
    return instrs, flag

def dead_code_elimination(instrs):
    flag = False
    used = set()
    for d in instrs:
        if not d['active']:
            continue
        if 'op1' in d and not is_num(d['op1']):
            used.add(d['op1'])
        if 'op2' in d and not is_num(d['op2']):
            used.add(d['op2'])
        if d['type'] == 'jump':
            for tok in re.findall(r'[A-Za-z_]\w*', d['raw']):
                used.add(tok)
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] in ('jump', 'label'):
            continue
        if 'result' in d and d['result'] not in used:
            if re.match(r'^t\d+$', d['result']):
                d['active'] = False
                flag = True
    return instrs, flag

def cse(instrs):
    flag = False
    seen = {}
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] == 'binary':
            key = (d['op1'], d['op'], d['op2'])
            key2 = None
            if d['op'] in ('+', '*'):
                key2 = (d['op2'], d['op'], d['op1'])
            if key in seen:
                d['op1'] = seen[key]
                d['type'] = 'copy'
                d.pop('op', None)
                d.pop('op2', None)
                flag = True
            elif key2 and key2 in seen:
                d['op1'] = seen[key2]
                d['type'] = 'copy'
                d.pop('op', None)
                d.pop('op2', None)
                flag = True
            else:
                seen[key] = d['result']
        if 'result' in d:
            remove = [k for k in seen if k[0] == d['result'] or k[2] == d['result']]
            for k in remove:
                del seen[k]
    return instrs, flag

def strength_reduction(instrs):
    flag = False
    for d in instrs:
        if not d['active']:
            continue
        if d['type'] != 'binary':
            continue
        a = d['op1']
        b = d['op2']
        op = d['op']
        if op == '*' and b == '1':
            d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '*' and a == '1':
            d['op1'] = b; d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '*' and b == '2':
            d['op2'] = d['op1']; d['op'] = '+'; flag = True
        elif op == '+' and b == '0':
            d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '+' and a == '0':
            d['op1'] = b; d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '-' and b == '0':
            d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '/' and b == '1':
            d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
        elif op == '*' and (a == '0' or b == '0'):
            d['op1'] = '0'; d['type'] = 'copy'; d.pop('op', None); d.pop('op2', None); flag = True
    return instrs, flag

def run_optimization(instrs):
    applied = []
    instrs, f = constant_folding(instrs)
    if f: applied.append("Constant Folding")
    instrs, f = constant_propagation(instrs)
    if f: applied.append("Constant Propagation")
    instrs, f = copy_propagation(instrs)
    if f: applied.append("Copy Propagation")
    instrs, f = cse(instrs)
    if f: applied.append("Common Subexpression Elimination")
    instrs, f = strength_reduction(instrs)
    if f: applied.append("Strength Reduction")
    instrs, f = dead_code_elimination(instrs)
    if f: applied.append("Dead Code Elimination")
    return instrs, applied


print("Code Optimization - Custom Input")
print("=" * 40)
print("Enter TAC lines one by one. Press Enter on empty line to stop.")
print("Format: t1 = a + b  or  x = t1  or  t2 = 3 * 4")
print()

lines = []
n = 1
while True:
    line = input("Line " + str(n) + ": ").strip()
    if line == "":
        break
    lines.append(line)
    n += 1

if lines:
    instrs = [parse_line(l) for l in lines]
    print_code(instrs, "Before Optimization:")
    instrs2 = [parse_line(l) for l in lines]
    instrs2, applied = run_optimization(instrs2)
    print_code(instrs2, "After Optimization:")
    print("Techniques applied: " + (", ".join(applied) if applied else "None"))
else:
    print("No input given.")
