# ethernet-frame-decoding

A few Python scripts for decoding Ethernet (10baseT) frames.

Usage:

```
./rigol_to_audacity.py RigolExport.csv audacity.txt

# You can open audacity.txt in Audacity now
# using Generate -> Sample Data Import... dialog

./ethernet_decode.py audacity.txt frame.dat payload.dat

# The scripts outputs binary data to stdout...

# Check frame CRC:
sudo pacman -S perl-archive-zip
crc32 frame.dat

# Also you can open payload.dat in Wireshark
# using Fime -> Import from Hex Dump dialog.

od -Ax -tx1 -v payload.dat  > payload.hex
```
