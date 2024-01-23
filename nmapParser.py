#!/bin/python
import sys,os,re,subprocess

def main():

    # Declare and initialize our variables
    target = "scanme.nmap.org"
    nmapOut = "/tmp/nmap.out"
    nmapRep = "/tmp/" + target + ".txt"

    # Define RegEx for IP addresses
    ip_ptrn = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    # Create the files if they do not exist yet 
    # Nmap output file
    nmapRaw = open(nmapOut, "a")
    nmapRaw.close() 

    # Parsed report file
    nmapPar = open(nmapRep, "a")
    nmapPar.close() 

    # Run the Nmap scan
    nmap = subprocess.run(["nmap","-sC", "-sV", target], capture_output=True, text=True)

    # Open the raw Nmap output file and store the data to be parsed
    nmapRaw = open(nmapOut, "w")
    nmapRaw.write(nmap.stdout)
    nmapRaw.close()
   
    # Open the parsed report file for writing
    nmapPar = open(nmapRep, "w")

    # Read a line from the output string and write it to the console
    # and parsed output file
    with open(nmapOut,"r") as nmap_output:
        for linex in nmap_output:
            
            if("Nmap scan report" in linex):
                print(" ")
                nmapPar.write(" \n")
                print(ip_ptrn.search(linex).group())
                nmapPar.write(ip_ptrn.search(linex).group() + "\n")
                print("-" * 20)
                nmapPar.write("-" * 20 + "\n")
            else:
                if("/tcp" in linex):
                    print(linex.split()[0] + ", " + linex.split()[2] + ", " + linex[30:-1])
                    nmapPar.write(linex.split()[0] + ", " + linex.split()[2] + ", " + linex[30:-1] + "\n")

    nmap_output.close()
    nmapPar.close()
    
if __name__ == '__main__':
    main()
