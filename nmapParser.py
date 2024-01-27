#!/bin/python
import re,subprocess,os

# Declare and initialize global variables
targetsFile = "/tmp/targets.txt"
target = "127.0.0.1"
nmapOut = ""
nmapRep = "" # The parsed nmap report
nmapPar = ""
nmapRaw = "" # The raw nmap output
ports=[]
targetList=[]

# Define RegEx for IP addresses and to remove protocol from targets
ip_ptrn = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
protoPrefix = re.compile(r'http:')
protoPrefixS = re.compile(r'https:')

class ccolors:
    G0 = '\u001b[38;5;40m'
    G1 = '\u001b[38;5;41m'
    G2 = '\u001b[38;5;42m'
    G3 = '\u001b[38;5;43m'
    G4 = '\u001b[38;5;44m'
    G5 = '\u001b[38;5;45m'
    G6 = '\u001b[38;5;50m'
    G7 = '\u001b[38;5;51m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKRED = '\u001b[31;1m'        
    ENDC = '\033[0m'

def initFiles(targetName):
    # Create the files if they do not exist yet 
    # Nmap output file
    print(ccolors.OKRED + "[+] Creating raw Nmap output file for " + ccolors.ENDC + targetName)
    nmapRaw = open(("/tmp/"+targetName+".nmap"), "a")
    nmapRaw.close() 

    # Parsed report file
    print(ccolors.OKRED + "[+] Creating parsed Nmap output file for " + ccolors.ENDC + targetName)
    nmapRep = open("/tmp/" + targetName + ".report", "a")
    nmapRep.close() 

def chkTargetFile():
    # Check if targets file exists and has content
    if (os.path.exists(targetsFile) == False):
        print(ccolors.OKRED + "[!] The targets file does not exist" + ccolors.ENDC)
        print(ccolors.OKRED + "\t- ensure that /tmp/targets.txt is present " + ccolors.ENDC)
        print(ccolors.OKRED + "\t- quitting " + ccolors.ENDC)
        exit()

    if (os.stat(targetsFile).st_size==0):
        print(ccolors.OKRED + "[!] The targets file is empty" + ccolors.ENDC)
        print(ccolors.OKRED + "\t- ensure that /tmp/targets.txt contains at least one target (IP or URL)" + ccolors.ENDC)
        print(ccolors.OKRED + "\t- quitting " + ccolors.ENDC)
        exit()

def nmapScan(scanTarget):
    # Run the Nmap scan 
    print(ccolors.OKRED + "[+] Running Nmap scan on " + ccolors.ENDC + scanTarget)
    nmap = subprocess.run(["nmap","-sC", "-sV", scanTarget], capture_output=True, text=True)

    # Open the raw Nmap output file and store the data to be parsed
    #print(ccolors.OKRED + "[+] Reading raw Nmap output..." + ccolors.ENDC)
    print(ccolors.OKRED + "[+] Reading raw Nmap output for " + ccolors.ENDC +  scanTarget)
    nmapOut = open(("/tmp/" + scanTarget + ".nmap"), "w")
    nmapOut.write(nmap.stdout)
    nmapOut.close()
   
    # Open the parsed report file for writing
    nmapPar = open(("/tmp/" + scanTarget + ".report"), "w")
    #nmapPar = open(nmapRep, "w")

    # Read a line from the output string and write it to the console
    # and parsed output file
    print(ccolors.OKRED + "[+] Parsing and writing formatted Nmap output for " + ccolors.ENDC + scanTarget)
    with open(("/tmp/" + scanTarget + ".nmap") ,"r") as nmap_output:
        for linex in nmap_output:
            
            if("Nmap scan report" in linex):
                #print(" ")
                nmapPar.write(" \n")
                #print(ip_ptrn.search(linex).group())
                nmapPar.write(ip_ptrn.search(linex).group() + "\n")
                #print("-" * 20)
                nmapPar.write("-" * 20 + "\n")
            else:
                if("/tcp" in linex):
                    version = ""
                    if linex[30:-1] == "":
                        version = "Version Not Found"
                    print(ccolors.OKBLUE + linex.split()[0] + ccolors.ENDC + ccolors.OKGREEN + ": " + linex.split()[2] + ", " + linex[30:-1] + version + ccolors.ENDC)
                    nmapPar.write(linex.split()[0] + ", " + linex.split()[2] + ", " + linex[30:-1] + version + "\n")
                    ports.append(linex.split()[0].split("/")[0])
    print(" ")
    print(" ")
    nmap_output.close()
    nmapPar.close()

def runTests(portList):
    # This function runs through the list of discovered ports
    # Each port associated with preconfigured commands will trigger
    # a call to a subroutine to either run or, more likely, build 
    # a script that can be run
    for portx in portList:
        print("testing port " + portx)
        if (portx == "80") or (portx == "443"):
            testHTTP(portx)

def readTargets(targFile, targList):
    with open(targFile,"r") as tFile:
        for linex in tFile:
            targetList.append(linex.rstrip())


def testHTTP(httpPort):
    print(ccolors.OKRED + "\t[+] Running http/s scan on "+ ccolors.OKBLUE + target+":"+httpPort + ccolors.ENDC + "\n")

def printBanner():
    banner = ccolors.G0 + "                _        __  __             \n"
    banner += ccolors.G1 + "     /\        | |      |  \/  |           \n" 
    banner += ccolors.G2 + "    /  \  _   _| |_ ___ | \  / | __ _ _ __  \n"
    banner += ccolors.G3 + "   / /\ \| | | | __/ _ \| |\/| |/ _` | '_ \ \n"
    banner += ccolors.G4 + "  / ____ \ |_| | || (_) | |  | | (_| | |_) |\n"
    banner += ccolors.G5 + " /_/    \_\__,_|\__\___/|_|  |_|\__,_| .__/ \n" 
    banner += ccolors.G6 + "                                     | |    \n"
    banner += ccolors.G7 + "                                     |_|    \n"
    banner += ccolors.OKGREEN + "                                      v0.1        \n" + ccolors.ENDC

    print(banner)

def main():
    subprocess.run(["clear"])

    printBanner() # Can't not have an ASCII art banner

    chkTargetFile() # Check that the target file exists and contains something

    readTargets(targetsFile, targetList)

    for xTarget in targetList:
        targetDom = xTarget

        if(protoPrefix.search(xTarget)):
            targetDom = (xTarget[7:])
        
        if(protoPrefixS.search(xTarget)):
            targetDom = (xTarget[8:])

        initFiles(targetDom) # Initialize files, clear out existing files and create empty ones
        nmapScan(targetDom) # Nmap scan the targets

    exit()

    print("\n" + ("-" * 20) + "\n")
    print(ccolors.OKRED + "\n[+] Starting individual port tests...\n" + ccolors.ENDC)

    runTests(ports)
    
if __name__ == '__main__':
    main()
