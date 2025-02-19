import re
import sys
import io

def cap():
    buf = io.StringIO()
    sys.stdout = buf
    return buf

def res():
    sys.stdout = sys.__stdout__

def clen(te):
    lines = []
    r, c = 0, 0
    ansi_p = re.compile(r'\x1b\[(\d+);(\d+)H')
    last_end=0
    for match in ansi_p.finditer(te):
        n_r = int(match.group(1)) -1
        n_c = int(match.group(2)) -1
        seg = te[last_end:match.start()]
        while len(lines) <= r:
            lines.append([])
        
        while len(lines[r]) <= c:
            lines[r].append(" ")

        for char in seg:
            if c >= len(lines[r]):
                lines[r].append(" ")
            lines[r][c] = char
            c += 1
        r, c = n_r, n_c
        last_end = match.end()

    r_te = te[last_end:]
    while len(lines) <= r:
        lines.append([])

    for char in r_te:
            while c >= len(lines[r]):
                lines[r].append(" ")
            lines[r][c] = char
            c += 1

    resul_lines = ["".join(line).rstrip() for line in lines]

    return "\n".join(resul_lines).rstrip()

b = cap()

print("Texto normal")
print('\x1b[2;1H\n   0   0   0   0\n   0   4   0   0\n   0   0   0   0\n   0   4   0   0\n\x1b[11;21H╭───╮\x1b[12;21H│ 0 │\x1b[13;21H╰───╯\x1b[11;26H╭───╮\x1b[12;26H│ 0 │\x1b[13;26H╰───╯\x1b[11;31H╭───╮\x1b[12;31H│ 0 │\x1b[13;31H╰───╯\x1b[11;36H╭───╮\x1b[12;36H│ 0 │\x1b[13;36H╰───╯\x1b[14;21H╭───╮\x1b[15;21H│ 0 │\x1b[16;21H╰───╯\x1b[14;26H╭───╮\x1b[15;26H│ 4 │\x1b[16;26H╰───╯\x1b[14;31H╭───╮\x1b[15;31H│ 0 │\x1b[16;31H╰───╯\x1b[14;36H╭───╮\x1b[15;36H│ 0 │\x1b[16;36H╰───╯\x1b[17;21H╭───╮\x1b[18;21H│ 0 │\x1b[19;21H╰───╯\x1b[17;26H╭───╮\x1b[18;26H│ 0 │\x1b[19;26H╰───╯\x1b[17;31H╭───╮\x1b[18;31H│ 0 │\x1b[19;31H╰───╯\x1b[17;36H╭───╮\x1b[18;36H│ 0 │\x1b[19;36H╰───╯\x1b[20;21H╭───╮\x1b[21;21H│ 0 │\x1b[22;21H╰───╯\x1b[20;26H╭───╮\x1b[21;26H│ 4 │\x1b[22;26H╰───╯\x1b[20;31H╭───╮\x1b[21;31H│ 0 │\x1b[22;31H╰───╯\x1b[20;36H╭───╮\x1b[21;36H│ 0 │\x1b[22;36H╰───╯\n'
)
print('\x1b[5;5HMensaje flotante')

c = b.getvalue()

res()

te_c = clen(c)

print("Texto virtualizado:")
print(te_c)