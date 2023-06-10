#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import logging

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

file1 = open(cidlog, "w")
file1.write(data1 + " = " + data2 + "\n")
file1.close()
