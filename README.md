# PAIN – Purely Abusive Instruction-less Notation

An attempt at making a programming language without defined instructions and (kind of) succeeding?

---

## What is PAIN?

PAIN is a self-mutating, instruction-less esolang where:

- **Program = memory = tape = instruction set**
- Every pair of bytes `(C1, C2)` is read sequentially

The program consumes itself as it runs, leaving behind a scarred, unrecognizable tape. Every run is unique unless you fight it into submission.

---

## Specification

### Memory Model
- The program text **is the memory**.
- Execution reads pairs `(C1, C2)` from left to right.
- A pointer `head` tracks the current pair.
- **Wrap-around applies**: jumping past program boundaries loops back.

---

### Rules

#### 1. SAME Pair (C1 == C2)

| Case                          | Effect                                          |
|-------------------------------|-------------------------------------------------|
| Printable (ASCII 32–126, 10)  | Print `C1`                                      |
| Non-printable                 | Move pointer backward by `C1` (wraps around)    |

```text
head = (head - C1) % program_length
```
---

#### 2. DIFFERENCE Pair (C1 != C2)

Mutate `C2` with:
```
diff = C2 - C1 + 1
new_C2 = (C2 + diff) % 256
```
Or expanded:
```
new_C2 = (2*C2 - C1 + 1) % 256
```
This mutation:

- Flips parity (odd ↔ even)

- Guarantees any ASCII is reachable

- Infects future execution with chaos

---

#### 3. Termination

Execution ends if:

- The pointer jumps to its current position (infinite loop)

---

## Special Notes

- Each byte participates in exactly two operations (as C1 and C2)

- Programs are one dense line unless `newline` byte is desired

- Bytes are single-byte values, wrapping around % 256

- The starting program is intended to only have printable characters, meaning hand typing a program is very much possible...

- PAIN isn't turing complete. I know, I know, it's hard to believe but it's true! We can't change the size of the tape which means we don't have infinite memory which is a requirement of turing completeness.

---

## Example: Hello, World!\n

Program:
```PAIN
nW $HHVehllmoM,-' ;WXdoprsplmidB!0?$
2Z
```
Output:
```
Hello, World!
```

#### Side Notes

- The program was hand written by yours truly. It took me **TWO** hours...

- The newline in the source code is intentional for printing and mutation.

- The start and end of the program contain bytes for the special purpose of making sure the program terminates when it wraps around for the second turn by making a NULL jump (to the current place) since only printable characters are allowed in the source code, we had to do special preparations to mutate two NULL bytes next to each other which will terminate the program on the second run. You can copy the same trick to run in any other program.

---

## Running PAIN

### Requirements
```
Python 3
```
Or implement it yourself. The spec is small enough...


### Example
```
python pain.py -f [File]
```
OR
```
python pain.py [Code]
```
OR
```
python pain.py -f [File] -d
```

### Arguments

- -f `[File]`       = Specify a file to run.

- -i `[Code]`       = Specify the code to run.

- -r `[Count]`      = Specify the number of times the program loops. Keep it `-1` or don't touch it for the default PAIN experience. Helps in debugging.

- -d                = Helps debug the program, hopefully...
