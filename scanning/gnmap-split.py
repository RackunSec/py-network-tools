#!/usr/bin/env python3
## 2022 - @RackunSec
## This script 
##  1. creates a new log directory in the current working directory
##  2. reads the gnmap file
##  3. creates files in the log directory for each protocol listed in GnmapOrg.protocols below.
## I made this to make my life easier and it worked.
##
from sys import argv,exit ## CLI args and Exit
from os import path,mkdir ## File Path Check
from re import search,sub ## Regexp

## Usage for app. Just pass me a .gnmap file:
def usage():
    print(f"[i] Usage: python3 gnmap-split.py (Nmap.gnmap file)")
    exit() ## done.

class GnmapOrg():
    def __init__(self,filename):
        self.protocols = {
            "ftp":{"port":[20,21],"hosts":[]},
            "smb":{"port":[445,139],"hosts":[]},
            "http":{"port":[80,8080],"hosts":[]},
            "https":{"port":[443,8443],"hosts":[]},
            "ldap":{"port":[389,636],"hosts":[]},
            "ssh":{"port":[22],"hosts":[]},
            "rdp":{"port":[3389],"hosts":[]},
            "netbios":{"port":[137,138,139],"hosts":[]},
            "sip":{"port":[5060],"hosts":[]},
            "vnc":{"port":[5900],"hosts":[]},
            "dns":{"port":[53],"hosts":[]},
            "telnet":{"port":[23],"hosts":[]},
            "smtp":{"port":[25,465,587],"hosts":[]},
            "kerberos":{"port":[88],"hosts":[]},
            "mysql":{"port":[3306],"hosts":[]},
            "oracle":{"port":[1521],"hosts":[]},
            "pop3":{"port":[995,109,110],"hosts":[]},
            "ipmi":{"port":[623],"hosts":[]},
            "ike":{"port":[500],"hosts":[]},
            "snmp":{"port":[161],"hosts":[]},
            "mssql":{"port":[1433],"hosts":[]},
            "winrm":{"port":[5985],"hosts":[]}
            }
        self.filename = filename

    def parse_file(self):
        self.check_file_exists()
        with open(self.filename,"r") as gnmap_contents:
            gnmap_lines = gnmap_contents.readlines()
            ## Loop pver the gnmap lines and build protocols{}
            for line in gnmap_lines: ## Loop over file and build protocols{}
                line_stripped = line.strip() ## remove newlines
                for proto in self.protocols:
                    for port in self.protocols[proto]['port']:
                        if search(f" {port}.open",line_stripped):
                            ## split the line and grab just the ip address:
                            host=line_stripped.split()[1]
                            if host not in self.protocols[proto]['hosts']:
                                self.protocols[proto]['hosts'].append(host)
            ## Now we write the log files:
            if "/" in argv[1]: ## They are running this from another directory:
                log_dir = sub(r".*\/([^.]+)\.gnmap",r"\1",argv[1]) ## make a directory
            else:
                log_dir = sub(r"([^.])\.gnmap",r"\1",argv[1])
            print(f"[i] Creating log directory: {log_dir}")
            if not path.isdir(log_dir):
                mkdir(log_dir)
            for proto in self.protocols: ## Loop over protocols and make log files
                if len(self.protocols[proto]['hosts'])>0: ## We have protocols to log
                    log_file = log_dir+"/"+proto+".txt"
                    if not path.exists(log_file): ## make the file
                        with open(log_file,"w") as write_log_file:
                            for host in self.protocols[proto]['hosts']:
                                write_log_file.write(host+"\n")
            print(f"[i] Completed.")


    def check_file_exists(self):
        if path.exists(self.filename):
            return True
        else:
            self.error(f"Could not open file: {self.filename}")
            exit() ## Done.

## Main() function of app:
def main():
    if len(argv)<2:
        usage()
    else:
        gnmaporg=GnmapOrg(argv[1])
        gnmaporg.parse_file()
 
if __name__=="__main__":
    main()
