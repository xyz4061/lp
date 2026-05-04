Macro Processor — Dependencies

File you run                  Also needs (auto-imported)
---------------------------------------------------------
mnt.py                       data.py + pass1.py
mdt.py                       data.py + pass1.py
intermediate_code.py         data.py + pass1.py
formal_positional.py         data.py + pass1.py
actual_positional.py         data.py + pass1.py + pass2.py
pass2.py (expanded code)     data.py + pass1.py
main.py                      everything above