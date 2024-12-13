#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(description="Automate subdomain enumeration and vulnerability checks.")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., google.com)")
    parser.add_argument("-o", "--output", default=".", help="Output folder path (default: current directory)")
    return parser.parse_args()

def create_output_directory(output_path, domain):
    domain_folder = os.path.join(output_path, f"{domain}_results")
    os.makedirs(domain_folder, exist_ok=True)
    print(f"[+] Created output directory: {domain_folder}")
    return domain_folder

def run_subdomain_enumeration(domain, output_dir):
    """
    Runs Knockpy, Subfinder, and Assetfinder in separate xterm terminals.
    Waits for all enumeration tools to complete before proceeding.
    """
    print("[*] Starting subdomain enumeration...")

    # Command for Knockpy
    knockpy_cmd = f"knockpy -d {domain} --recon --bruteforce && jq -r '.[].domain' *.json > domains.txt"
    xterm_knockpy = ["xterm", "-e", knockpy_cmd]

    # Command for Subfinder
    subfinder_cmd = f"subfinder -d {domain} -all -o domains2.txt"
    xterm_subfinder = ["xterm", "-e", subfinder_cmd]

    # Command for Assetfinder
    assetfinder_cmd = f"assetfinder --subs-only {domain} > domains3.txt"
    xterm_assetfinder = ["xterm", "-e", assetfinder_cmd]

    # Launch all three enumeration tools in separate xterm windows
    try:
        process_knockpy = subprocess.Popen(xterm_knockpy, cwd=output_dir)
        process_subfinder = subprocess.Popen(xterm_subfinder, cwd=output_dir)
        process_assetfinder = subprocess.Popen(xterm_assetfinder, cwd=output_dir)
        print("[+] Launched Knockpy, Subfinder, and Assetfinder in separate xterm windows.")

        # Wait for all enumeration tools to complete
        process_knockpy.wait()
        process_subfinder.wait()
        process_assetfinder.wait()
        print("[+] Subdomain enumeration completed.")

    except FileNotFoundError as e:
        print(f"[!] Terminal emulator not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Failed to launch enumeration tools: {e}")
        sys.exit(1)

def merge_subdomains(output_dir):
    """
    Merges all subdomain files and removes duplicates.
    """
    print("[*] Merging subdomain results...")
    merge_cmd = "sort -u domains.txt domains2.txt domains3.txt > allsubdomain.txt"
    try:
        subprocess.run(merge_cmd, shell=True, cwd=output_dir, check=True)
        print("[+] Merged subdomains into allsubdomain.txt")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to merge subdomains: {e}")
        sys.exit(1)

def run_subzy(output_dir):
    """
    Runs Subzy in a new gnome-terminal and keeps the terminal open.
    """
    print("[*] Starting Subzy for subdomain takeover vulnerability checks...")
    subzy_cmd = "subzy run --targets allsubdomain.txt"
    gnome_cmd = f"gnome-terminal -- bash -c \"{subzy_cmd}; exec bash\""
    try:
        subprocess.Popen(gnome_cmd, cwd=output_dir, shell=True)
        print("[+] Launched Subzy in a new gnome-terminal.")
    except Exception as e:
        print(f"[!] Failed to launch Subzy: {e}")
        sys.exit(1)

def check_alive_subdomains(output_dir):
    """
    Checks alive subdomains using httpx.
    """
    print("[*] Checking alive subdomains with httpx...")
    httpx_cmd = "httpx -l allsubdomain.txt -o alivesubdomain.txt"
    try:
        subprocess.run(httpx_cmd, shell=True, cwd=output_dir, check=True)
        print("[+] Alive subdomains saved to alivesubdomain.txt")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to check alive subdomains: {e}")
        sys.exit(1)

def check_alive_with_statuscode(output_dir):
    """
    Checks alive subdomains with status codes using httpx in a new gnome-terminal.
    """
    print("[*] Checking alive subdomains with status codes...")
    statuscode_cmd = "httpx -l alivesubdomain.txt -sc -o alivedomainsstatuscode.txt"
    gnome_cmd = f"gnome-terminal -- bash -c \"{statuscode_cmd}; exec bash\""
    try:
        subprocess.Popen(gnome_cmd, cwd=output_dir, shell=True)
        print("[+] Launched httpx for status codes in a new gnome-terminal.")
    except Exception as e:
        print(f"[!] Failed to launch httpx for status codes: {e}")
        sys.exit(1)

def main():
    args = parse_arguments()
    domain = args.domain
    output_path = os.path.abspath(args.output)

    # Create output directory
    output_dir = create_output_directory(output_path, domain)

    # Step 1: Subdomain Enumeration
    run_subdomain_enumeration(domain, output_dir)

    # Step 2: Merge subdomains and remove duplicates
    merge_subdomains(output_dir)

    # Step 3: Check subdomain takeover vulnerabilities (Subzy)
    run_subzy(output_dir)

    # Step 4: Check alive subdomains with httpx
    check_alive_subdomains(output_dir)

    # Step 5: Check alive subdomains with status codes
    check_alive_with_statuscode(output_dir)

    print("\n[+] Automation completed successfully.")

if __name__ == "__main__":
    main()
