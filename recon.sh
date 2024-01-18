#!/bin/bash
domain=$1
RED="\033[1;31m"
RESET="\033[0m"

subs_path=$domain/subs
screens_path=$domain/screens
scan_path=$domain/scans

if [ ! -d "$domain" ]; then
   mkdir $domain
fi

for path in subs screens scans
do
  if [ ! -d "$domain/$path" ]; then
     mkdir $domain/$path
  fi
done

echo -e "${RED} [+] launching subfinder... ${RESET}"
subfinder -d $domain > $subs_path/found.txt

echo -e "${RED} [+] launching assetfinder... ${RESET}"
assetfinder $domain | grep $domain >> $subs_path/found.txt

#echo -e "${RED} [+] launching amass... ${RESET}"
#amass enum -d $domain >> $subs_path/found.txt

echo -e "${RED} [+] finding live subdomains... ${RESET}"
cat $subs_path/found.txt | grep $domain | sort -u | httprobe -prefer-https | grep https | sed 's/https\?:\/\///' | tee -a $subs_path/live.txt

echo -e "${RED} [+] taking screenshots of live subs... ${RESET}"
gowitness file -f $subs_path/live.txt -P $screens_path/ --no-http

echo -e "${RED} [+] running nmap on live subs... ${RESET}"
nmap -iL $subs_path/live.txt -T4 -A -p- -oN $scan_path/nmap.txt
