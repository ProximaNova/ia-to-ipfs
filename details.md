# Explaining a command

## Command

`cd ../$v1+*; v1=$(expr $v1 + 1); echo -n "$v1 out of $v2 at "; pwd; h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> $path4; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 $path4; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 $path4 | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> $path5; tail -n1 $path5`

In the updated version, part of it is replaced with `grep "<subject>" | sed "s/;/,/g" | perl -pE "s/\n/, /g" | perl -pE "s/, $/\n/g" | sed "s/ \? \?<\/\?subject>//g"`.

## Explained

`cd ../$v1+*`
- Change directory to "../$v1+[...]", an adjacent folder which is current folder index number plus one, a plus sign, then the ID

`v1=$(expr $v1 + 1); echo -n "$v1 out of $v2 at "`
- Set $v1 to itself plus one. Echo $v1 out of $v2. Variable $v2 is the non-recursive count of the folders in .. minus about 3. The echo command should probably come before the variable value assignment command.

`pwd`
- "Part" of echo "# out of # at current/working directory"

`h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g")`
- Set $h1 to current folder (string) but replace "[...]+" with "https://archive.org/details/". I can probably chage stuff so it does not have to process it as a URL (just use the ID).

`h2=$(ipfs add -rHQ .)`
- Set $h2 to the resulting CID of the current folder, recursively, including hidden files. -Q just returns the CID to stdout and no other details.

`h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2)`
- Set $h3 to "$h2 [CIDv0] = [CIDv1]". I should probably use more descriptive variable names.

`echo $h3 >> $path4`
- Append $h3 to $path4, which is file "cids.txt"

`ipfs ls $h2 | head -n 5`
- Look inside folder $h2 (a v0 CID) and show 5 of its folders or files

`ipfs pin add $h2 > /dev/null`
- Pin $h2 and do not show some or all of the output.

`find . -type f -delete; find . -type d -delete`
- Delete all files and folders in the current directory since they should be in IPFS now. In the future, maybe I will make an option to keep files, be careful deleting files (extra checks or something), and/or put files in trash at ".Trash.000" or whatever.

`tail -n 3 $path4`
- Show the last three lines of cids.txt

`h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 $path4 | sed "s/.* //g")`
- Set $h00 to some text
- Echo "`<li>[$h1 but the ID only]: [ipfs:// hyperlink with link name being a v1 CID]`"
- `tail -n1 $path4 | sed "s/.* //g"` I think is the bottom right "keyword" of cids.txt.
- Text `tail -n1 $path4 | sed "s/.* //g"` could probably be simplified to `ipfs cid base32 $h2`

`h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>")`
- Set $h5 to some text
- `h4=$(echo $h1 | sed "s/.*\///g")` - set $h4 to $h1 but the ID only
- `echo -n $h00; echo -n '">'` - echo the first part of a list item and hyperlink ($h00) then the next part of the hyperlink
- `ipfs cat $h2/"$h4"_meta.xml | grep "<title>"` - search [CIDv0]/[ID]_meta.xml and return line matching "`<title>`", piped into the next command
- `sed "s/ \? \?<\/\?title>//g" | tr -d \\n` - remove "[zero or one space here][zero or one space here]<[zero or one forward slash here]title>" and newlines
- `echo -n "</a> - "` - close the hyperlink
- `ipfs cat $h2/"$h4"_meta.xml | grep "<subject>"` - search file "[CIDv0]/[ID]_meta.xml" and return line(s) matching "`<subject>`", piped into the next command
- `sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"` - replace ";" with "," then remove "[zero or one space here x 2]<[zero or one forward slash here]subject>" and newlines then close the list item

`echo $h5 >> $path5; tail -n1 $path5`
- Append $h5 ("bunch of text") to index.html then show the last line of index.html
