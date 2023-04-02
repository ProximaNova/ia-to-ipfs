# ia-to-ipfs
Convert Internet Archive items to IPFS: these commands help convert data under https://archive.org/details/[ID] into IPFS CIDs.

Please note that this is currently a low-effort thing, so use at your own risk and understand the commands and/or code.

## Reasons
1. In 2023-02-05 the Internet Archive implemented even more cringe censorship, so if an item is loginwalled you can download it and provide unrestricted access to it if the CID is seeded enough. 
2. This is helpful to organize files and have them indexed in an HTML file.
3. Use this to support the decentralized web, which could potential have more uptime than Internet Archive (IA).

## Requirements
1. GNU/Linux, I was using Ubuntu and the Bash shell
2. This script: https://github.com/john-corcoran/internetarchive-downloader - was copied to https://github.com/ProximaNova/ia-to-ipfs/tree/main/internetarchive-downloader
3. Prerequisites and requirements as stated in "john-corcoran/internetarchive-downloader" and "john-corcoran/internetarchive-downloader/requirements.txt"
4. InterPlanetary File System (IPFS): https://ipfs.tech/#install

## Usage
1. Open a terminal program (CLI).
2. Make a text file ("ids.txt") which contains IA item IDs, one ID per line. Said ID is the text after https://archive.org/details/ - so the TXT file could look like this:
```
youtube-T8Xsi0Dne8o
20040106-bbs-veggie
youtube-19oYvXhQbWc
```
3. Set a variable to the list of IA item IDs that you want to download. Run `path1=/path/to/ids.txt`.
4. Set a variable to 1; this is the folder index number. Run `foldernumber=1`.
5. Set another variable to 1; this is the line index number, so which line in ids.txt to pull an ID from. Run `linenumber=1`.
6. Create two text files. One that contains your archive.org login email address: "s1.txt". One that contains your archive.org login password in plain text: "s2.txt". These are used to download login-required archive.org items. If you want to delete these s* files later, run `shred -u [filename]`. For more important OPSEC info, see john-corcoran/internetarchive-downloader/README.md
7. Set variables to the secret files. Run `path2=/path/to/s1.txt` and `path3=/path/to/s2.txt`.
8. Run `cd /path/to/a/completely/empty/folder/` - then add ia_downloader.py to this folder (can also be ran via `python3 ia_downloader.py [...]`).
9. Run ia_downloader.py, maybe with "--threads 1" and "--resume". What I ran: `v4=$(tail -n +$linenumber $path1 | head -n 1); date -u; ./ia_downloader.py download -i $v4 --credentials "$(cat $path2)" "$(cat $path3)" --output "$foldernumber+$v4"; date -u; cd "$foldernumber+$v4"; v3=$(ls); cd $v3; echo "Moving..."; mv -n * ..; date -u; cd ..; rm -R $v3; cd ..; echo "foldernumber: $foldernumber"; echo "linenumber: $linenumber"; foldernumber=$(expr $foldernumber + 1); linenumber=$(expr $linenumber + 1)`
10. Run `!!; !!` - or however many more `; !!` you need for the number of items you want to download. Understand that `!!; !!` runs the previous command twice, so if you ran any commands after the previous command that could be bad.
11. After downloading the items that you want, check for any issues by running `grep -liar KeyboardInterrupt ./ia_downloader_logs/logs` and `grep -liar ConnectionError/ReadTimeout ./ia_downloader_logs/logs` and `find . -maxdepth 1 -type d -empty`. "KeyboardInterrupt" means that you hit ctrl+c or maybe ctrl+z before ia_downloader finished processing an item. "ConnectionError/ReadTimeout" means that the connection was unstable and you had trouble downloading the item. An empty folder might mean that ia_downloader was unable to download any files (if "ConnectionError/ReadTimeout" is returned, the program will retry like 4 times, and it will not keep retrying until the file is downloaded).
12. Run `cd 1+*`
13. Run something like this: `v2=$(find .. -maxdepth 1 -type d | sort | tail -n +3 | wc -l); v1=2` - v2 is roughly the total folders/items you downloaded and v1 is the index number of the next folder.
14. Make empty text files "cids.txt" and "index.html". cids.txt contains a list of CIDs in two formats. index.html is an HTML file where LI elements will be added to it. After you add some LI tags to it you can add the text that goes at the top of HTML documents to it to make it more valid (such as the TITLE tag). Don't add ending HTML document tags and stuff to the .html file.
15. Set variables to those two files. Run `path4=/path/to/cids.txt` and `path5=/path/to/index.html`.
16. Run `h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> $path4; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 $path4; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 $path4 | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | perl -pE "s/\n/, /g" | perl -pE "s/, $/\n/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> $path5; tail -n1 $path5`
17. Run `cd ../$v1+*; v1=$(expr $v1 + 1); echo -n "$v1 out of $v2 at "; pwd; h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> $path4; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 $path4; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 $path4 | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | perl -pE "s/\n/, /g" | perl -pE "s/, $/\n/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> $path5; tail -n1 $path5`
18. Run `!!; !!` - or however many more `; !!` you need (e.g., `!!; !!; !!; !!; !!; !!`) for the number of items you want to pin.

## Bugs and problems
* I saw it move up too many directories one time (could have bad results - see `rm -R` above), don't know what caused that
* All $path* variables must not contain spaces
* When adding to IPFS, cancel via one or more ctrl+c then redo the previous command skips over the unfinished current folder and goes to work on the next one.
* Commands could be better or more simple
* Usage could be made easier
* IPFS CIDs don't have enough feed and sneed. Make an account at https://www.pinata.cloud/ and https://web3.storage/ because Pinata and w3s can help seed smaller pinsets.
* Bugs/problems as stated in github.com/john-corcoran/internetarchive-downloader
* Instead of downloading everything first then running ipfs, it could be changed to download an item then pin it, download the next item then pin it, etc. Doing this versus how it is currently done depends on how much the items are at risk of being deleted off of Internet Archive; the current method assumes that uploads are at-risk.
* Does not seem to be a big problem, but something to keep an eye on: "[ipfs: datetime:] ERROR provider.queue queue/queue.go:125 Failed to enqueue cid: leveldb: closed"
* If file "*_meta.xml" contains HTML entities then it messes up how the XML file is parsed. Example from index number 2234, identifier 736...f74: source_code=`<subject>tag1; tag2; text &amp; text; a &amp; b; tag3; tag4</subject>`, rendered_xml=`<subject>tag1; tag2; text & text; a & b; tag3; tag4</subject>`, parsed_text_for_html=`tag1, tag2, text &amp, text, a &amp, b, tag3, tag4`, what_parsed_text_for_html_should_look_like=`tag1, tag2, text &amp;, text, a &amp;, b, tag3, tag4`

Fixed?:
<br>&#x2a; Messes up if a filename of a file in archive.org starts with a hyphen (-)
<br>&#x2a;&#x2a; Untested fix: `v4=$(tail -n +$linenumber $path1 | head -n 1); date -u; ./ia_downloader.py download -i $v4 --credentials "$(cat $path2)" "$(cat $path3)" --output "$foldernumber+$v4"; date -u; cd "$foldernumber+$v4"; v3=$(ls); cd ./$v3; echo "Moving..."; mv -n ./* ..; date -u; cd ..; rm -R ./$v3; cd ..; echo "foldernumber: $foldernumber"; echo "linenumber: $linenumber"; foldernumber=$(expr $foldernumber + 1); linenumber=$(expr $linenumber + 1)`

Fixed (probably):
<br>&#x2a; Might not work if file `[...]_meta.xml` contains multiple subject fields.
<br>&#x2a;&#x2a; Tested fix: `cat /path/to/itemid_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; cat /path/to/itemid_meta.xml | grep "<subject>" | sed "s/;/,/g" | perl -pE "s/\n/, /g" | perl -pE "s/, $/\n/g" | sed "s/ \? \?<\/\?subject>//g"`
<br>&#x2a;&#x2a;&#x2a; Tested with multiple subject fields in index number 1863, identifier 653...332
