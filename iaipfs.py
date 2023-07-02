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

# -- Run "./iaipfs.py -h" for help text.
# -- ./iaipfs.py -h might say "optional arguments"
# -- on the third line of output. That is is incorrect,
# -- for only -p is optional.

parser = argparse.ArgumentParser()
# -- pin or not, folder to add, cid log, item index
parser.add_argument("-p", "--pin", action="store_true",
    required=False, help="""(Optional) if specified,
    this pins the CID; pin it if you want to keep the
    data for a long time.""")
parser.add_argument("-f", "--folder", type=str,
    required=True, help="""Path to the folder which only
    contains data from one IA item, the folder's name
    should be the item identifier. Make sure that the
    path works properly when wrapped in double quote
    characters (\") - e.g., no '!' character in Linux.
    Paths under the folder (like filenames in the IA item)
    can have whatever characters, so don't worry about those
    files' names.""")
parser.add_argument("-c", "--cidlog", type=str,
    required=True, help="""Initially empty text file to
    log the CIDs in. Make sure that the path works properly
    when wrapped in double quote characters.""")
parser.add_argument("-x", "--htmlindex", type=str,
    required=True, help="""Initially empty text file to
    contain some HTML data which acts as an index of IA
    items in IPFS. Path should work when wrapped in
    double quotes.""")
args = parser.parse_args()
folder = args.folder
folderfolder = os.path.dirname(folder)
folderpath = pathlib.Path(folder)
folderlast = folderpath.name
cidlog = args.cidlog
htmlindex = args.htmlindex
tempfile = cidlog + ".1686364707.temp"

print("Folder: " + folder)
print("CID log: " + cidlog)
print("HTML index: " + htmlindex)

cmd="ipfs add -rHQ \"" + folder + "\" > \"" + tempfile + "\""
os.system(cmd)

with open(tempfile, "r") as file:
    data1 = file.read().rstrip()

cmd="ipfs cid base32 " + data1 + " > \"" + tempfile + "\""
os.system(cmd)

with open(tempfile, "r") as file:
    data2 = file.read().rstrip()

file1 = open(cidlog, "a")
file1.write(data1 + " = " + data2 + "\n")
file1.close()
# -- dedup cid
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

cmd="ipfs cat " + data1 + "/" + folderlast + "_meta.xml > \"" + tempfile + "\""
os.system(cmd)

subject = ""
with open(tempfile, "r") as file3:
    for line5 in file3:
        match = re.search("<title>.*", line5)
        if match:
            title = re.findall("<title>.*", line5)
        match2 = re.search("<subject>.*", line5)
        if match2:
            subject += str(re.findall("<subject>.*", line5))
file3.close()
# -- doesn't work well if both ' and " are in subject or title, works if one or the other is in the title or subject
title2 = re.sub("\[?'?\"?<\/?title>\"?'?\]?", "", str(title))
subject2 = re.sub("<\/subject>'?\"?\]\['?\"?<subject>", "; ", str(subject))
subject3 = re.sub("\[?'?\"?<\/?subject>\"?'?\]?", "", str(subject2))

file4 = open(htmlindex, "a")
file4.write("<li>" + folderlast + ": <a href=\"ipfs://" + data2 + "\">" + title2 + "</a> - " + re.sub(";", ",", subject3) + "</li>\n")
file4.close()
# -- dedup html
file1 = open(htmlindex, "r")
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
    file1 = open(htmlindex, "w")
    file1.write(data3)
    file1.close()

if args.pin:
    cmd="ipfs pin add " + data1
    os.system(cmd)
