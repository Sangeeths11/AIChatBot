# Run this to install the required packages


# ----------------------------
# / / / WORK IN PROGRESS / / /
# ----------------------------

import subprocess

# Check if the 'pip' command is available
try:
    subprocess.check_output(["pip", "--version"])
except FileNotFoundError:
    raise Exception("Python's 'pip' is not installed. Please install it and try again.")

# Install required packages
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])

print("All required packages have been successfully installed.")