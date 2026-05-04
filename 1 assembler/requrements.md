Assembler — same pattern

File you run            Also needs
------------------------------------------------
symbol_table.py         data.py + pass1.py
literal_table.py        data.py + pass1.py
pool_table.py           data.py + pass1.py
intermediate_code.py    data.py + pass1.py
errors.py               data.py + pass1.py
main.py                 everything above


Same rule — always data.py + pass1.py,
everything else is self-contained.