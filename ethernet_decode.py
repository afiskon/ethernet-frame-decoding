#!/usr/bin/env python3
# vim: set ai et ts=4 sw=4:

import sys

if len(sys.argv) < 4:
    print("Usage: " + sys.argv[0] + " input.txt frame.dat payload.dat")
    sys.exit(1)

infile = sys.argv[1]
framefile = sys.argv[2]
payloadfile = sys.argv[3]
peak_threshold = 0.1
step_threshold = 0.25
peak_reports = 50
eps = 0.01
vmin = -1.0
vmax = 1.0

frame = b'' # Ethernet frame without preamble and CRC
payload = b''
total_bytes = 0
output_buff = ""
def output(n):
    global output_buff, total_bytes, frame, payload
    assert(n == 0 or n == 1)
    output_buff += str(n)
    if len(output_buff) == 8:
        byte = int(output_buff[::-1], 2)
        bytehex = "0x{:02X}".format(byte)
        print("%s # %s" % (output_buff, bytehex))
        output_buff = ""
        if total_bytes >= 8:
            frame += bytes([ byte ])
        if total_bytes >= 22:
            payload += bytes([ byte ])
        total_bytes += 1

nline = 0
pos_start = neg_start = -1
step = -1
last_peak = 0
last_peak_pos = False
steps_sum = 0

with open(infile) as fin:
    for line in fin:
        nline += 1
        val = float(line)
        if peak_reports > 0: # calculating approximate step size
            if (vmax - val)/vmax < peak_threshold:
                # print("Pos peak at sample %d" % (nline))
                if pos_start == -1:
                    pos_start = nline
                    last_peak = nline
                    last_peak_pos = True
                    output(0) # neg -> pos transition is 0
                peak_reports -= 1
            if (vmin - val)/vmin < peak_threshold:
                # print("Neg peak at sample %d" % (nline))
                if neg_start == -1:
                    neg_start = nline
                    last_peak = nline
                    last_peak_pos = False
                    output(1) # pos -> neg transition is 1
                peak_reports -= 1
            if peak_reports == 0:
               step = abs(neg_start - pos_start) # /2
               # print("Step: ~ %d samples" % (step))
        else: # peak_reports == 0, decoding data
            is_pos_peak = (vmax - val)/vmax < peak_threshold
            is_neg_peak = (vmin - val)/vmin < peak_threshold
            assert(not (is_pos_peak and is_neg_peak))

            if (is_pos_peak and (not last_peak_pos)) or (is_neg_peak and last_peak_pos):
                step_delta = ((nline - last_peak)/step)
                if abs(1.0 - step_delta) < step_threshold:
                    step_delta = 1.0
                elif abs(0.5 - step_delta) < step_threshold:
                    step_delta = 0.5
                else:
                    raise Exception("Unexpected step delta %.02f" % (step_delta))

                steps_sum += step_delta
                assert(steps_sum <= 1.0 + eps)

                # print("%s peak, %.02f step" % ("Pos" if is_pos_peak else "Neg", (nline - last_peak)/step))

                if abs(steps_sum - 1.0) < eps: # process one full step
                    # neg -> pos transition is 0
                    # pos -> neg transition is 1
                    output(0 if is_pos_peak else 1)
                    steps_sum = 0.0

                last_peak = nline
                last_peak_pos = is_pos_peak

assert(output_buff == "")

payload = payload[:-4] # cut CRC in the end of data
frame = frame[:-4]

with open(framefile, mode = 'wb') as fout:
    fout.write(frame)

with open(payloadfile, mode = 'wb') as fout:
    fout.write(payload)

print("\ndone!")
