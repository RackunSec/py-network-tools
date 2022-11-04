# Gnmap-Split: a Gnmap File Organizer
Gnmap-Split will take the output of Nmap's (often very large) GNmap file and organize it for usage with red team tools that require lists of IP addresses. For instance, This tool will create an output directory full of files labeled after the identified protocol: "ftp.txt" or "ldap.txt" that can then be passed as arguments into tools such as CrackMapExec, SMBMap, etc.

## Usage
To use ScanSplit:
```bash
python3 gnmap-split.py /path/to/nmap-output.gnmap
```
