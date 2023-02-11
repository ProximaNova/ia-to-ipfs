# ia-to-ipfs
Convert Internet Archive items to IPFS: these commands help convert data under https://archive.org/details/[ID] into IPFS CIDs.

## Reasons
1. In 2023-02-05 the Internet Archive instigated even more cringe censorship, so if an item is loginwalled you can download it and provide unrestricted access to it if the CID is seeded enough. 
2. This is helpful to organize files and have them indexed in an HTML file.
3. Use this to support the decentralized web, which could potential have more uptime than Internet Archive (IA).

## Requirements
1. GNU/Linux, I was using Ubuntu and the Bash shell
3. This script: https://github.com/john-corcoran/internetarchive-downloader - was copied to https://github.com/ProximaNova/ia-to-ipfs/tree/main/internetarchive-downloader
4. Prerequisites and requirements as stated in "john-corcoran/internetarchive-downloader" and "john-corcoran/internetarchive-downloader/requirements.txt"
5. IPFS: https://ipfs.tech/#install

## Usage
Please note that this is currently a low-effort thing, so use at your own risk and understand the "code".

1. Open a terminal program (CLI).
2. Make a text file ("ids.txt") which contains IA item IDs, one ID per line. Said ID is the text after https://archive.org/details/ - so the TXT file could look like this:
```
youtube-T8Xsi0Dne8o
20040106-bbs-veggie
youtube-19oYvXhQbWc
```
3. Set a variable to the list of IA item IDs that you want to download. Run `path1=/path/to/ids`.
4. Set a variable to 1; this is the folder index number. Run `foldernumber=1`.
5. Set another variable to 1; this is the line index number, so which line in ids.txt to pull an ID from. Run `linenumber=1`.
6. Create two text files. One that contains your archive.org login email address: "s1.txt". One that contains your archive.org login password in plain text: "s2.txt". These are used to download login-required archive.org items. If you want to delete these s* files later, run `shred -u [filename]`. For more important OPSEC info, see john-corcoran/internetarchive-downloader/README.md
7. Set variables to the secret files. Run `path2=/path/to/s1` and `path3=/path/to/s2`.
8. Run `cd /path/to/a/completely/empty/folder/` - then add ia_downloader.py to this folder (can also be ran via `python3 ia_downloader.py [...]`).
9. Run ia_downloader.py, maybe with "--threads 1" and "--resume". What I ran: `v4=$(tail -n +$linenumber $path1/ids.txt | head -n 1); date -u; ./ia_downloader.py download -i $v4 --credentials "$(cat $path2/s1.txt)" "$(cat $path3/s2.txt)" --output "$foldernumber+$v4"; date -u; cd "$foldernumber+$v4"; v3=$(ls); cd $v3; echo "Moving..."; mv -n * ..; date -u; cd ..; rm -R $v3; cd ..; echo "foldernumber: $foldernumber"; echo "linenumber: $linenumber"; foldernumber=$(expr $foldernumber + 1); linenumber=$(expr $linenumber + 1)`
10. Run "!!; !!" - or however many more "; !!" you need for the number of items you want to download. Understand that "!!; !!" runs the previous command twice, so if you ran any commands after the previous command that could be bad.
11. After downloading the items that you want, run `cd 1+*`
12. Run something like this: `v2=$(find .. -maxdepth 1 -type d | sort | tail -n +3 | wc -l); v1=2` - v2 is roughly the total folders/items you downloaded and v1 is the index number of the next folder.
13. Make text files "cids.txt" and "index.html".
14. Run `h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> /path/to/cids.txt; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 /path/to/cids.txt; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 /path/to/cids.txt | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> /path/to/index.html; tail -n1 /path/to/index.html`
15. Run `cd ../$v1+*; v1=$(expr $v1 + 1); echo -n "$v1 out of $v2 at "; pwd; h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> /path/to/cids.txt; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 /path/to/cids.txt; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 /path/to/cids.txt | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> /path/to/index.html; tail -n1 /path/to/index.html`
16. Run "!!; !!" - or however many more "; !!" you need for the number of items you want to pin.

## Bugs and problems
* Commands could be better or more simple
* Usage could be made easier
* Messes up if a filename of a file in archive.org starts with a hyphen (-)
* I saw it move up too many directories one time (could have bad results), don't know what caused that
* IPFS CIDs don't have enough sneed and feed. Make an account at https://www.pinata.cloud/ because Pinata can help seed smaller pinsets.
