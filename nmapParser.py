import sys,os,re

def main():
    ip_ptrn = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    
    
    with open("nmap.out","r") as nmap_output:
        for linex in nmap_output:
            
            if("Nmap scan report" in linex):
                print(" ")
                print(ip_ptrn.search(linex).group())
                print("-" * 20)
            else:
                if("/tcp" in linex):
                    print(linex.split()[0] + ", " + linex.split()[2] + ", " + linex[30:-1])

    nmap_output.close()
    
if __name__ == '__main__':
    main()
