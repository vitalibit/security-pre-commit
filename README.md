# Gitleaks Pre-commit Hook

This script sets up a pre-commit hook for Git that automatically checks for secrets in your code using Gitleaks.

## Prerequisites

- Python 3
- Git
- Curl (for installation)

## Installation

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the cloned repository.
3. Run the following command to install Python 3 and Gitleaks:

```shell
python3 setup.py
```

Follow the on-screen instructions to complete the installation process.
Configuration
By default, the pre-commit hook is enabled. To disable it, run the following command:

shell
Copy code
git config gitleaks.enabled false
To enable the pre-commit hook, run the following command:

shell
Copy code
git config gitleaks.enabled true
Usage
Once the pre-commit hook is enabled, it will automatically run Gitleaks before each commit. If any secrets are found, the commit will be rejected.

To manually run Gitleaks without committing, you can use the following command:

shell
Copy code
gitleaks --repo-path /path/to/your/repository
Make sure to replace /path/to/your/repository with the actual path to your repository.
