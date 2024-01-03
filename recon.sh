#!/bin/bash
domain=$1
RED="\033[1;31m"
RESET="\033[0m"

subdomain_path=$domain/subdomains
screenshot_path=$domain/screenshots
scan_path=$domain/scans

if [ ! -d "$domain" ]; then
   mkdir $domain
fi

for pathx in subdomains screenshots scans
do
  if [ ! -d "$domain/pathx" ]; then
     mkdir $domain/pathx
  fi
done

echo -e "${RED} [+] launching subfinder... ${RESET}"
subfinder -d $domain > $subdomain_path/found.txt

echo -e "${RED} [+] launching assetfinder... ${RESET}"
assetfinder $domain | grep $domain >> $subdomain_path/found.txt

#echo -e "${RED} [+] launching amass... ${RESET}"
#amass enum -d $domain >> $subdomain_path/found.txt

echo -e "${RED} [+] finding live subdomains... ${RESET}"
cat $subdomain_path/found.txt | grep $domain | sort -u | httprobe -perfer-https | grep https | sed 's/https\?:\/\/// | tee -a $subdomain_path/live.txt

echo -e "${RED} [+] taking screenshots of live subs... ${RESET}"
gowitness file -f $subdomain_path/live.txt -P $screenshot_path/ --no-http

echo -e "${RED} [+] running nmap on live subs... ${RESET}"
nmap -iL $subdomain_path/live.txt -T4 -A -p- -oN $scan_path/nmap.txt
