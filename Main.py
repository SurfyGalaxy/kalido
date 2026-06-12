"""
- Escape sequences start with \x1b
- CSI sequences usually start with \x1b[
- CSI sequences end with a single final byte in @ A-Z [ \\ ] ^ _ ` a-z ~
- If the final byte is 'm', the sequence is a colour/style code (SGR)
    → discard the entire sequence
- Otherwise, preserve the sequence unchanged
- Everything outside escape sequences is normal printable text
"""

import sys
import functions as func
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
stops = func.create_gradient(stops, count)
index = 0

while True:
    c = sys.stdin.read(1)
    if not c:
        break

    if STATE == "NORMAL":
        if c == "\x1b":
            STATE = "ESC"
            seq = c
        else:
            sys.stdout.write(func.colourise(stops, c, index))
            if index == len(stops) -1:
                index = 0
            else:
                index += 1

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