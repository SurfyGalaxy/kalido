"""
- Escape sequences start with \x1b
- CSI sequences usually start with \x1b[
- CSI sequences end with a single final byte in @ A-Z [ \ ] ^ _ ` a-z ~
- If the final byte is 'm', the sequence is a colour/style code (SGR)
    → discard the entire sequence
- Otherwise, preserve the sequence unchanged
- Everything outside escape sequences is normal printable text
"""

import sys
import argparse

STATE = "NORMAL"
seq = ""
rgb_stops = []

parser = argparse.ArgumentParser()

parser.add_argument(
    "--stops",
    nargs="+",
    default=["#E40303", "#FF8C00", "#FFED00", "#008026", "#004CFF", "#732982"],
    help="gradient color stops (hex values)",
)
parser.add_argument(
    "--count",
    type=int,
    default=20,
    help="The amount of intermediate values to add between stops",
)
args = parser.parse_args()
stops = args.stops
count = args.count
# This is a list of hex codes with the # still

stops = [code[1:] for code in stops] # Strip the leading # to make my life easier

for code in stops:
    red = int(code[:2], 16)
    green = int(code[2:4], 16)
    blue = int(code[4:], 16)
    rgb_stops.append((red, green, blue))
print(rgb_stops)

while True:
    c = sys.stdin.read(1)
    if not c:
        break

    if STATE == "NORMAL":
        if c == "\x1b":
            STATE = "ESC"
            seq = c
        else:
            # I presume colouriser goes here?
            sys.stdout.write(c)

    elif STATE == "ESC":
        seq += c

        if c == "[":
            STATE = "CSI"
        else:
            # not CSI, just output and reset
            sys.stdout.write(seq)
            STATE = "NORMAL"

    elif STATE == "CSI":
        seq += c

        if '@' <= c <= '~':  # final byte

            if c != "m":
                sys.stdout.write(seq)  # keep non-colour sequences

            # always reset once
            STATE = "NORMAL"
            seq = ""