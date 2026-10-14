from sys import argv

input_buffer = []
output_buffer = []


def putchar(char):
    print(char, end='')

def run_pain(program, repeat = 1, debug = False):
    prev_ptr = 0
    ptr = 0
    prog = list(program);
    offset = 1

    while prog:
        log = ""
        prev_ptr = ptr
        if repeat == 0:
            if debug: print("Exiting...")
            break

        c1 = ord(prog[ptr])
        nextPtr = (ptr + 1) % len(prog)
        c2 = ord(prog[nextPtr])
        diff = c2 - c1

        log += f"REPETITIONS LEFT: {repeat if repeat >= 0 else '∞'}\n"
        log += f"[POS = {ptr}] ('{chr(c1)}', '{chr(c2)}'): DIFF = {diff}, PROG_LEN = {len(prog)}\n"

        if c1 == c2:
            # SAME-pair: print current char if printable
            if 32 <= c1 <= 126 or c1 == 10:
                output_buffer.append(chr(c1))
                if not debug: putchar(chr(c1))
                log += f"OP: putchar('{chr(c1)}')\n"
            # SAME-pair: jump back by c1 otherwise
            else:
                ptr = ptr - c1
                log += f"OP: jumpBackBy({c1}), newPos = {ptr+1}\n"
                # If jumped to the same location, end program
                if prev_ptr == ptr:
                    log += "OP: exit()\n"
                    prog = ""
        else:
            # Mutate next char
            new_c2 = (c2 + diff + offset) % 256
            prog[nextPtr] = chr(new_c2)
            log += f"OP: mutateNext(next: '{chr(c2)}', offset: {diff}), newNext = '{chr(new_c2) if 32 <= new_c2 <= 126 else f'ASCII({new_c2})'}'\n"
        
        if ptr + 1 >= len(prog) and repeat > 0:
            repeat -= 1

        # Move forward and wrap it
        if prog: ptr = (ptr + 1) % len(prog)

        log += f"OUTPUT: \"{''.join(output_buffer)}\"\n"

        if debug:
            print(log)


code = ""
repeat = -1
debug = False

if '-f' in argv and len(argv) > argv.index('-f') + 1:
    with open(argv[argv.index('-f')+1], 'r') as f: code = f.read()
    code = code[:len(code) - 1]
if '-i' in argv and len(argv) > argv.index('-i') + 1:
    code = argv[argv.index('-i')+1]
if '-r' in argv and len(argv) > argv.index('-r') + 1:
    repeat = int(argv[argv.index('-r')+1])
if '-d' in argv:
    debug = True
if len(argv) == 2:
    try:
        with open(argv[1], 'r') as f: code = f.read()
        code = code[:len(code) - 1]
    except FileNotFoundError:
        code = argv[1]
if len(argv) == 1:
    print(f"Usage: {argv[0]} [-i|-f|-r|code|file] [code|file]")


run_pain(code, repeat, debug)
