# ============================================================
#  pass1.py  –  Pass 1 of Macro Processor
#
#  Reads source, builds MNT and MDT.
#  Intermediate code = source lines with macro definitions removed.
#  Formal parameters replaced with positional notation (#1, #2 ...)
#  Nested macro calls inside a definition are expanded early (MDT stores
#  the expanded body with actual args substituted as positional refs).
# ============================================================

import os
import data

_dir        = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(_dir, "sample.asm")


def run_pass1(source_lines):
    """
    Single-pass over source.
    - Recognises MACRO ... MEND blocks → fills MNT + MDT
    - Everything outside a definition → INTERMEDIATE code
    """
    i = 0
    lines = [l.rstrip('\n') for l in source_lines]

    while i < len(lines):
        line = lines[i].strip()

        # ── Skip blank lines ──────────────────────────────
        if not line:
            i += 1
            continue

        tokens = line.split()

        # ── MACRO definition starts ───────────────────────
        if tokens[0].upper() == "MACRO":
            # MACRO  name  [p1, p2, ...]
            macro_name   = tokens[1].upper() if len(tokens) > 1 else ""
            # collect formal params (strip commas)
            formal_params = [t.rstrip(',') for t in tokens[2:]]
            num_params    = len(formal_params)
            mdt_start     = len(data.MDT) + 1   # 1-based index

            # Register in MNT  (store formal_params too)
            data.MNT.append({
                'name':         macro_name,
                'num_params':   num_params,
                'mdt_index':    mdt_start,
                'formal_params': formal_params
            })

            # ── Formal vs Positional table entry ─────────
            fp_entry = {'macro': macro_name, 'params': []}
            for idx, fp in enumerate(formal_params, 1):
                fp_entry['params'].append({'formal': fp, 'positional': f'#{idx}'})
            data.FORMAL_POSITIONAL.append(fp_entry)

            # Read body until MEND
            i += 1
            while i < len(lines):
                body_line = lines[i].strip()
                i += 1
                if not body_line:
                    continue
                if body_line.upper() == "MEND":
                    data.MDT.append("MEND")
                    break

                # Replace formal params with positional notation
                body_tokens = body_line.split()
                replaced    = []
                for tok in body_tokens:
                    tok_clean = tok.rstrip(',')
                    if tok_clean in formal_params:
                        pos = formal_params.index(tok_clean) + 1
                        replaced.append(f"#{pos}")
                    else:
                        replaced.append(tok)

                # Check if this body line is a call to another macro
                # (nested macro call – expand early: substitute literal args)
                call_name = replaced[0].upper()
                nested_mnt = _find_macro(call_name)

                if nested_mnt:
                    # actual args passed to nested call
                    actual_args = [a.rstrip(',') for a in replaced[1:]]
                    # expand nested macro body into MDT
                    _expand_nested(nested_mnt, actual_args)
                else:
                    data.MDT.append(" ".join(replaced))

        # ── END ───────────────────────────────────────────
        elif tokens[0].upper() == "END":
            data.INTERMEDIATE.append(line)
            break

        # ── Normal source line (outside any macro def) ────
        else:
            data.INTERMEDIATE.append(line)
            i += 1
            continue

    # (loop already incremented i inside MACRO block)


def _find_macro(name):
    """Return MNT entry dict for given macro name, or None."""
    for entry in data.MNT:
        if entry['name'] == name.upper():
            return entry
    return None


def _expand_nested(mnt_entry, actual_args):
    """
    Expand a nested macro call inside a macro body.
    Writes expanded lines into MDT, substituting actual_args for #N.
    Stops at MEND (does not write MEND for the nested call).
    """
    start = mnt_entry['mdt_index'] - 1   # 0-based
    for mdt_line in data.MDT[start:]:
        if mdt_line == "MEND":
            break
        # substitute #N with actual arg or keep as-is
        parts = mdt_line.split()
        new_parts = []
        for p in parts:
            if p.startswith('#'):
                try:
                    idx = int(p[1:]) - 1
                    new_parts.append(actual_args[idx] if idx < len(actual_args) else p)
                except ValueError:
                    new_parts.append(p)
            else:
                new_parts.append(p)
        data.MDT.append(" ".join(new_parts))


# ── Standalone run ────────────────────────────────────────────

if __name__ == "__main__":
    try:
        with open(SOURCE_FILE) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File '{SOURCE_FILE}' not found.")
        exit(1)

    run_pass1(lines)

    print("\n[Pass 1 complete]")
    print(f"  Macros defined : {len(data.MNT)}")
    print(f"  MDT entries    : {len(data.MDT)}")
    print(f"  IC lines       : {len(data.INTERMEDIATE)}")
    if data.ERRORS:
        print("\nErrors:")
        for e in data.ERRORS:
            print(f"  {e}")
