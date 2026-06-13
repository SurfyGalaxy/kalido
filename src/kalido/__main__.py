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
import os
import pathlib
import yaml
import functions as func
import argparse
import random

script_dir = pathlib.Path(__file__).parent
presets_path = script_dir / "presets.yaml"
with open(presets_path) as f: # Copied from my other project, Clide
    presets = yaml.safe_load(f)

STATE = "NORMAL"
seq = ""
rgb_stops = []

sys.stdout.reconfigure(line_buffering=True)
parser = argparse.ArgumentParser()

parser.add_argument(
    "--stops",
    nargs="+",
    default=["random"],
    help="gradient color stops (hex values)",
)
parser.add_argument(
    "--count",
    type=int,
    default=20,
    help="The amount of intermediate values to add between stops",
)
parser.add_argument(
    "--size",
    type=int,
    default=5,
    help="How large each colour is before moving to next colour"
)
args = parser.parse_args()
stops = args.stops
count = args.count
size = args.size
# This is a list of hex codes with the # still

if stops[0] in presets:
    stops = presets[stops[0]]
elif stops[0] == "random":
    random_flag = random.choice(list(presets.keys()))
    stops = presets[random_flag]

    

stops = func.create_gradient(stops, count + 1)
index = 0
size_index = size

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
            sys.stdout.flush()
            if size_index != 1:
                size_index -= 1
            else:
                if index == len(stops) -1:
                    index = 0
                else:
                    index += 1
                size_index = size

    elif STATE == "ESC":
        seq += c

        if c == "[":
            STATE = "CSI"
        else:
            # not CSI, just output and reset
            sys.stdout.write(seq)
            sys.stdout.flush()
            STATE = "NORMAL"

    elif STATE == "CSI":
        seq += c

        if '@' <= c <= '~':  # final byte

            if c != "m":
                sys.stdout.write(seq)  # keep non-colour sequences
                sys.stdout.flush()

            # always reset once
            STATE = "NORMAL"
            seq = ""

sys.stdout.write('\n')
sys.stdout.flush()