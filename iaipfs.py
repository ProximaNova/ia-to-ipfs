#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import logging
import pathlib
import os.path
from os.path import exists
# from datetime import datetime
# from datetime import timezone
# import time
import re

parser = argparse.ArgumentParser()
# -- folder to add
parser.add_argument("-f", "--folder", type=str)
# -- cid log
parser.add_argument("-c", "--cidlog", type=str)
# -- item index
parser.add_argument("-x", "--htmlindex", type=str)
args = parser.parse_args()
folder = args.folder
folderfolder = os.path.dirname(folder)
folderpath = pathlib.Path(folder)
folderlast = folderpath.name
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

# addedunix = data1 + "_in_ipfs_" + str(time.time())
# os.rename(folder, os.path.join(folderfolder, addedunix))

cmd="ipfs cat " + data1 + "/" + folderlast + "_meta.xml > " + tempfile
os.system(cmd)

with open(tempfile, "r") as file3:
    for line5 in file3:
        match = re.search("<title>.*", line5)
        if match:
            title = re.findall("<title>.*", line5)
        match2 = re.search("<subject>.*", line5)
        if match2:
            subject = re.findall("<subject>.*", line5)
file3.close()
title2 = re.sub("\[?'?<\/?title>'?\]?", "", str(title))
subject2 = re.sub("\[?'?<\/?subject>'?\]?", "", str(subject))

file4 = open(htmlindex, "a")
file4.write("<li>" + folderlast + ": <a href=\"ipfs://" + data2 + "\">" + title2 + "</a> - " + subject2 + "</li>\n")
file4.close()
