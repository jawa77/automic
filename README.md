# Subdomain Enumeration and Vulnerability Checker

This automic tool automates subdomain enumeration and vulnerability checks using various tools like Knockpy, Subfinder, Assetfinder, Subzy, katana and Httpx.

## Features

- Automates subdomain enumeration using Knockpy, Subfinder, and Assetfinder.
- Merges results and removes duplicate entries.
- Checks subdomain takeover vulnerabilities using Subzy.
- Identifies alive subdomains and their status codes using Httpx.
- crawling sites and fetch urls
- Outputs results in organized files.

## Pre-requisites

Make sure the following tools are installed on your system:

1. [Knockpy](https://github.com/guelfoweb/knock)
2. [Subfinder](https://github.com/projectdiscovery/subfinder)
3. [Assetfinder](https://github.com/tomnomnom/assetfinder)
4. [Subzy](https://github.com/LukaSikic/subzy)
5. [Httpx](https://github.com/projectdiscovery/httpx)
6. `xterm` and `gnome-terminal` are required for terminal-based operations.
7. [katana](https://github.com/projectdiscovery/katana/cmd/katana)

## Installation

Run the provided `setup.sh` script to install all dependencies and tools automatically.

```bash
bash setup.sh
```

## Usage

Run the script using the following command:

```bash
python3 automic.py -d <target_domain> [-o <output_directory>]
```

- `-d` or `--domain`: Target domain (e.g., `google.com`). (Required)
- `-o` or `--output`: Output folder path. Defaults to the current directory.

### Example

```bash
python3 automic.py -d example.com -o results
```

## Outputs

The script generates the following files in the output directory:

1. `domains.txt`, `domains2.txt`, `domains3.txt`: Raw subdomain lists from enumeration tools.
2. `allsubdomain.txt`: Merged list of unique subdomains.
3. `alivesubdomain.txt`: Alive subdomains.
4. `alivedomainsstatuscode.txt`: Alive subdomains with HTTP status codes.
5. ` allurls.txt`: get all endurls from web

## License

MIT License
