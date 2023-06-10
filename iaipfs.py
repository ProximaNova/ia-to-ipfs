#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import logging
from os.path import exists

parser = argparse.ArgumentParser()
# -- folder to add
parser.add_argument("-f", "--folder", type=str)
# -- cid log
parser.add_argument("-c", "--cidlog", type=str)
# -- item index
parser.add_argument("-x", "--htmlindex", type=str)
args = parser.parse_args()
folder = args.folder
cidlog = args.cidlog
htmlindex = args.htmlindex
tempfile = cidlog + ".1686364707.temp"

# with open(cidlog, 'w') as sys.stdout: 

print("Folder: " + folder)
print("CID log: " + cidlog)
print("HTML index: " + htmlindex)

cmd="ipfs add -rHQ " + folder + " > " + tempfile
os.system(cmd)

with open(tempfile, "r") as file:
    data1 = file.read().rstrip()

cmd="ipfs cid base32 " + data1 + " > " + tempfile
os.system(cmd)

with open(tempfile, "r") as file:
    data2 = file.read().rstrip()

file1 = open(cidlog, "a")
file1.write(data1 + " = " + data2 + "\n")
file1.close()
file1 = open(cidlog, "r")
file2 = open(tempfile, "w")
line_dedup = set()
for line in file1:
    lines1 = line.rstrip().encode('utf-8')
    if lines1 not in line_dedup:
        file2.write(line)
        line_dedup.add(lines1)
file1.close()
file2.close()
with open(tempfile, "r") as file:
    data3 = file.read()
    file1 = open(cidlog, "w")
    file1.write(data3)
    file1.close()
