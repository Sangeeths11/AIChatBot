import shutil
import subprocess
import sys
import time
import webbrowser


# Function to run shell commands
def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing: {e.cmd}")
        sys.exit(1)

def setup_frontend():
    # 1. Check if Node.js is installed
    if not shutil.which("node"):
        print("Node.js is not installed. Please install it from https://nodejs.org/en/download/ and try again.")
        sys.exit(1)
    # 2. Install vue.js (vue-cli), yarn and nuxt.js (create-nuxt-app)
    print("Installing vue.js (vue-cli)")
    run_command("npm install -g @vue/cli")
    print("Installing yarn")
    run_command("npm install -g yarn")
    print("Installing nuxt.js (create-nuxt-app)")
    run_command("npm install -g create-nuxt-app")

    # 3. Create a new nuxt.js project
    run_command("cd aichatbot-nuxt && yarn add nuxt")
    print("All crated, we are ready to go. Let's start the app.")


def open_browser(backend_ready, frontend_ready):
    # Wait for both futures to be marked as ready
    backend_ready.result()
    frontend_ready.result()
    time.sleep(4)
    print("Opening browser...")
    webbrowser.open("http://localhost:3000/")
