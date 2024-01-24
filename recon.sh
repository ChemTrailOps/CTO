import sys,os,re,subprocess

def printBanner():
    class bcolors:
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        G0 = '\u001b[38;5;40m'
        G1 = '\u001b[38;5;41m'
        G2 = '\u001b[38;5;42m'
        G3 = '\u001b[38;5;43m'
        G4 = '\u001b[38;5;44m'
        G5 = '\u001b[38;5;45m'
        G6 = '\u001b[38;5;50m'
        G7 = '\u001b[38;5;51m'

    banner = bcolors.G0 + "                _        __  __             \n"
    banner += bcolors.G1 + "     /\        | |      |  \/  |           \n" 
    banner += bcolors.G2 + "    /  \  _   _| |_ ___ | \  / | __ _ _ __  \n"
    banner += bcolors.G3 + "   / /\ \| | | | __/ _ \| |\/| |/ _` | '_ \ \n"
    banner += bcolors.G4 + "  / ____ \ |_| | || (_) | |  | | (_| | |_) |\n"
    banner += bcolors.G5 + " /_/    \_\__,_|\__\___/|_|  |_|\__,_| .__/ \n" 
    banner += bcolors.G6 + "                                     | |    \n"
    banner += bcolors.G7 + "                                     |_|    \n"
    banner += bcolors.OKGREEN + "                                      v0.1        \n" + bcolors.ENDC

    print(banner)



def main():
    class bcolors:
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        OKRED = '\u001b[31;1m'        
        ENDC = '\033[0m'

    subprocess.run(["clear"])

    printBanner()

    # Declare and initialize our variables
    #target = "scanme.nmap.org"
    target = "example.com"
    nmapOut = "/tmp/nmap.out"
    nmapRep = "/tmp/" + target + ".txt"

    # Define RegEx for IP addresses
    ip_ptrn = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    # Create the files if they do not exist yet 
    # Nmap output file
    print(bcolors.OKRED + "[+] Creating raw Nmap output file..." + bcolors.ENDC)
    nmapRaw = open(nmapOut, "a")
    nmapRaw.close() 

    # Parsed report file
    print(bcolors.OKRED + "[+] Creating parsed Nmap output file..." + bcolors.ENDC)
    nmapPar = open(nmapRep, "a")
    nmapPar.close() 

    # Run the Nmap scan 
    print(bcolors.OKRED + "[+] Running Nmap scan..." + bcolors.ENDC)
    nmap = subprocess.run(["nmap","-sC", "-sV", target], capture_output=True, text=True)

    # Open the raw Nmap output file and store the data to be parsed
    print(bcolors.OKRED + "[+] Reading raw Nmap output..." + bcolors.ENDC)
    nmapRaw = open(nmapOut, "w")
    nmapRaw.write(nmap.stdout)
    nmapRaw.close()
   
    # Open the parsed report file for writing
    nmapPar = open(nmapRep, "w")

    # Read a line from the output string and write it to the console
    # and parsed output file
    print(bcolors.OKRED + "[+] Parsing and writing formatted Nmap output..." + bcolors.ENDC)
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
                    version = ""
                    if linex[30:-1] == "":
                        version = "Version Not Found"
                    print(bcolors.OKBLUE + linex.split()[0] + bcolors.ENDC + bcolors.OKGREEN + ": " + linex.split()[2] + ", " + linex[30:-1] + version + bcolors.ENDC)
                    nmapPar.write(linex.split()[0] + ", " + linex.split()[2] + ", " + linex[30:-1] + version + "\n")

    nmap_output.close()
    nmapPar.close()
    print(bcolors.OKRED + "\n\n\n[+] Done!\n\n\n" + bcolors.ENDC)
    
if __name__ == '__main__':
    main()
