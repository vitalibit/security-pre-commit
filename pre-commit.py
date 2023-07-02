#!/usr/bin/env python3

import os
import platform
import shutil
import subprocess
import sys

GITLEAKS_VERSION = "8.17.0"

def install_gitleaks():
    system = platform.system()
    machine = platform.machine()
    archive_filename = f"gitleaks_{GITLEAKS_VERSION}_"

    if system == "Linux":
        if machine == "arm64":
            archive_filename += "linux_arm64.tar.gz"
        else:
            archive_filename += "linux_x64.tar.gz"
    elif system == "Darwin":
        if machine == "arm64":
            archive_filename += "darwin_arm64.tar.gz"
        else:
            archive_filename += "darwin_x64.tar.gz"
    # elif system == "Windows":
    #     archive_filename = f"gitleaks-windows-amd64.exe"
    else:
        print(f"Error: Unsupported system {system}. Unable to install gitleaks.")
        sys.exit(1)

    download_url = f"https://github.com/gitleaks/gitleaks/releases/download/v{GITLEAKS_VERSION}/{archive_filename}"
    output_filename = "gitleaks"

    subprocess.run(["curl", "-sfL", download_url, "-o", output_filename], check=True)
    print("I download archive")
    subprocess.run(["tar", "-xzf", output_filename, output_filename], check=True)
    print ("I made tar command")

def enable_gitleaks_hook():
    enable_option = subprocess.run(["git", "config", "--get", "gitleaks.enabled"], capture_output=True, text=True).stdout.strip()
    enable = True
    if enable_option:
        enable = enable_option.lower() != "false"
    if enable:
        hooks_dir = os.path.join(".git", "hooks")
        pre_commit_script = os.path.join(hooks_dir, "pre-commit")
        script_path = os.path.abspath(__file__)
        
        if not os.path.exists(pre_commit_script):
            shutil.copy(script_path, pre_commit_script)
            subprocess.run(["chmod", "+x", pre_commit_script], check=True)
            print("Gitleaks pre-commit hook enabled.")
    else:
        print("Gitleaks pre-commit hook disabled.")


def check_for_secrets():
    try:
        subprocess.run(["./gitleaks", "version"], check=True)
    except FileNotFoundError:
        print("gitleaks not found. Installing...")
        install_gitleaks()

    command = ["./gitleaks", "detect", "--source", ".", "--verbose"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    print("Standard Output:")
    print(stdout)
    print("Standard Error:")
    print(stderr)

    if process.returncode != 0:
        print("Error: Secrets detected. Commit rejected.")
        sys.exit(1)

def main():
    # Check if Gitleaks is already installed
    gitleaks_path = "./gitleaks"
    print(f"Check if Gitleaks is already installed, gitleaks_path: {gitleaks_path}")
    if os.path.exists(gitleaks_path):
        installed_version = subprocess.run([gitleaks_path, "version"], capture_output=True, text=True).stdout.strip()
        if installed_version == GITLEAKS_VERSION:
            print(f"Gitleaks {GITLEAKS_VERSION} is already installed.")
        else:
            print(f"Existing Gitleaks version {installed_version} is not compatible. Installing Gitleaks {GITLEAKS_VERSION}...")
            install_gitleaks()
    else:
        print("Gitleaks is not installed. Installing...")
        install_gitleaks()

    # Enable gitleaks pre-commit hook
    enable_gitleaks_hook()

    # Check for secrets
    check_for_secrets()

if __name__ == "__main__":
    main()
