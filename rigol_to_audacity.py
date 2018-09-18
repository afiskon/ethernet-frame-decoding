#!/usr/bin/env python3
# vim: set ai et ts=4 sw=4:

import sys

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " input.csv output.txt")
    sys.exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

# First pass: find min and max values

vmin = float("+inf")
vmax = float("-inf")

nline = 0;
with open(infile) as fin:
    for line in fin:
        nline += 1
        if nline <= 2: # skip header
            continue
        strvals = line.split(",")
        val = float(strvals[1])
        vmax = max(val, vmax)
        vmin = min(val, vmin)

print("min: %.02f, max: %.02f" % (vmin, vmax))

# Second pass: convert rigol csv file to audacity txt file
nline = 0
with open(outfile, mode='w') as fout:
    with open(infile) as fin:
        for line in fin:
            nline += 1
            if nline <= 2: # skip header
                continue
            strvals = line.split(",")
            val = float(strvals[1])
            # convert to -1 .. 1 range
            val = ((val - vmin)/(vmax - vmin))*2 - 1
            fout.write(str(val) + "\n")

print("done!")
