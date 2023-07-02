#!/usr/bin/env python3

import os
import platform
import shutil
import subprocess
import sys

def install_python3():
    system = platform.system()
    if system == "Linux":
        subprocess.run(["sudo", "apt", "install", "python3"], check=True)
    elif system == "Darwin":
        subprocess.run(["brew", "install", "python@3"], check=True)
    elif system == "Windows":
        print("Please manually install Python 3 for Windows.")
    else:
        print(f"Error: Unsupported system {system}. Unable to install Python 3.")
        sys.exit(1)

def install_gitleaks():
    system = platform.system()
    if system == "Linux":
        subprocess.run(["curl", "-sfL", "https://github.com/zricethezav/gitleaks/releases/latest/download/gitleaks-linux-amd64", "-o", "gitleaks"], check=True)
    elif system == "Darwin":
        subprocess.run(["curl", "-sfL", "https://github.com/zricethezav/gitleaks/releases/latest/download/gitleaks-darwin-amd64", "-o", "gitleaks"], check=True)
    elif system == "Windows":
        subprocess.run(["curl", "-sfL", "https://github.com/zricethezav/gitleaks/releases/latest/download/gitleaks-windows-amd64.exe", "-o", "gitleaks.exe"], check=True)
    else:
        print(f"Error: Unsupported system {system}. Unable to install gitleaks.")
        sys.exit(1)

def enable_gitleaks_hook():
    enable_option = subprocess.run(["git", "config", "--get", "gitleaks.enabled"], capture_output=True, text=True).stdout.strip()
    enable = True
    if enable_option:
        enable = enable_option.lower() != "false"
    if enable:
        hooks_dir = os.path.join(".git", "hooks")
        pre_commit_script = os.path.join(hooks_dir, "pre-commit")
        script_path = os.path.abspath(__file__)
        shutil.copy(script_path, pre_commit_script)
        subprocess.run(["chmod", "+x", pre_commit_script], check=True)
        print("Gitleaks pre-commit hook enabled.")
    else:
        print("Gitleaks pre-commit hook disabled.")

def main():
    # Install Python 3 if it's not already installed
    python_version = sys.version_info
    if python_version.major < 3:
        print("Python 3 is required. Installing Python 3...")
        install_python3()

    # Install gitleaks
    install_gitleaks()

    # Enable gitleaks pre-commit hook
    enable_gitleaks_hook()

if __name__ == "__main__":
    main()