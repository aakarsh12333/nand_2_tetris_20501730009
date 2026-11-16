import sys
USER = {}      # labels and variables defined by the program
COMP = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101',
        '!A':'110001','-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110',
        'A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}
DEST = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
SYMBOLS = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576,
           **{f'R{i}':i for i in range(16)}}

def comp_bits(c):
    if 'M' in c:
        return '1' + COMP[c.replace('M', 'A')]
    return '0' + COMP[c]

def assemble(path):
    lines = []                                   # (line_number, cleaned_text)
    for n, raw in enumerate(open(path), 1):
        t = raw.split('//')[0].replace(' ', '').strip()
        if t:
            lines.append((n, t))

    # FIRST PASS: record labels
    rom = 0; code = []
    for n, t in lines:
        if t.startswith('(') and t.endswith(')'):
            label = t[1:-1]
            SYMBOLS[label] = rom                 # label = address of NEXT instruction
        else:
            code.append((n, t))
            rom += 1

    # SECOND PASS: translate
    nxt = 16; out = []
    for n, t in code:
        if t[0] == '@':
            s = t[1:]
            if s.isdigit(): v = int(s)
            else:
                if s not in SYMBOLS:
                    SYMBOLS[s] = nxt; nxt += 1   # new variable
                v = SYMBOLS[s]
            out.append(format(v, '016b'))
        else:
            d, c, j = '', t, ''
            if '=' in c: d, c = c.split('=')
            if ';' in c: c, j = c.split(';')
            out.append('111' + comp_bits(c) + DEST[d] + JUMP[j])
    return out

if __name__ == '__main__':
    src = sys.argv[1]
    open(src.replace('.asm', '.hack'), 'w').write('\n'.join(assemble(src)) + '\n')
    with open('symbols.txt', 'w') as f:
        for name, addr in USER.items():
            f.write(f'{name} = {addr}\n')