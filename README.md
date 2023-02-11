# ia-to-ipfs
Convert Internet Archive items to IPFS: these commands help convert data under https://archive.org/details/[ID] into IPFS CIDs.

## Reasons
1. In 2023-02-05 the Internet Archive instigated even more cringe censorship, so if an item is loginwalled you can download it and provide unrestricted access to it if the CID is seedeed enough. 
2. This is helpful to organize files and have them indexed in an HTML file.
3. Use this to support the decentralized web.

## Requirements
1. GNU/Linux, I was using Ubuntu and the Bash shell
3. This script: https://github.com/john-corcoran/internetarchive-downloader - was copied to https://github.com/ProximaNova/ia-to-ipfs/tree/main/internetarchive-downloader
4. Prerequisites and requirements as stated in "john-corcoran/internetarchive-downloader" and "john-corcoran/internetarchive-downloader/requirements.txt"
5. IPFS: https://ipfs.tech/#install

## Usage
Please note that this is currently a low-effort thing, so use at your own risk and understand the "code".

```
$ # set v5 and v6 to some number, s1.txt contains an email address, s2.txt contains a password, maybe use "--threads 1" and "--resume"
$ v4=$(tail -n +$v6 ids.txt | head -n 1); date; ./ia_downloader.py download -i $v4 --credentials "$(cat s1.txt)" "$(cat s2.txt)" --output "$v5+$v4"; date; cd "$v5+$v4"; v3=$(ls); cd $v3; echo "Moving..."; mv -n * ..; date; cd ..; rm -R $v3; cd ..; echo "v5: $v5"; echo "v6: $v6"; v5=$(expr $v5 + 1); v6=$(expr $v6 + 1)

$ cd /mnt/My_Passport/1/empty/z/include/1+*
$ v2=$(find .. -maxdepth 1 -type d | sort | tail -n +4 | wc -l); v1=2
$ h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> /mnt/My_Passport/b/ipfs/ipns/ia/mineis/index.html; tail -n1 /mnt/My_Passport/b/ipfs/ipns/ia/mineis/index.html
$ cd ../$v1+*; v1=$(expr $v1 + 1); echo -n "$v1 out of $v2 at "; pwd; h1=$(pwd | sed "s/.*+/https:\/\/archive.org\/details\//g"); h2=$(ipfs add -rHQ .); h3=$(echo -n $h2; echo -n " = "; ipfs cid base32 $h2); echo $h3 >> /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt; ipfs ls $h2 | head -n 5; ipfs pin add $h2 > /dev/null; find . -type f -delete; find . -type d -delete; tail -n 3 /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt; h00=$(echo -n '<li>'; echo -n "$h1" | sed "s/.*\///g"; echo -n ': <a href="ipfs://'; tail -n1 /mnt/My_Passport/b/ipfs/ipns/cid/cids.txt | sed "s/.* //g"); h5=$(h4=$(echo $h1 | sed "s/.*\///g"); echo -n $h00; echo -n '">'; ipfs cat $h2/"$h4"_meta.xml | grep "<title>" | sed "s/ \? \?<\/\?title>//g" | tr -d \\n; echo -n "</a> - "; ipfs cat $h2/"$h4"_meta.xml | grep "<subject>" | sed "s/;/,/g" | sed "s/ \? \?<\/\?subject>//g" | tr -d \\n; echo "</li>"); echo $h5 >> /mnt/My_Passport/b/ipfs/ipns/ia/mineis/index.html; tail -n1 /mnt/My_Passport/b/ipfs/ipns/ia/mineis/index.html
```
