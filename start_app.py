import base64
import subprocess
import sys
import os
import threading
from installRequiredments import setup_requirements
from Setup import setup_frontend, open_browser
from concurrent.futures import Future

def create_environment_variable_file():
    # Create the environment variable file if it doesn't exist
    if not os.path.exists('.env'):
        with open('env-cred', 'r') as creds_file:
            creds = creds_file.read()
        decoded_creds = base64.b64decode(creds).decode('utf-8')
        # Parse the JSON credentials
        # Write the credentials to a file
        with open('.env', 'w') as env_file:
            env_file.write(decoded_creds)

r = input("""Welcome to BrainWaive.
If this is the first you use this project, we'll need to install some dependencies and packages.
Shall we proceed?
If you already installed everything just continue with 'n'.
Proceed? y / n: """)
if r.lower() == 'n':
    print("Great! You already installed all packages for the backend.")
    r2 = input("Do you want to setup the frontend? y / n: ")
    if r2.lower() == 'y':
        setup_frontend()
    else:
        print("Okay, let's start the Application.")
elif r.lower() == 'y':
    create_environment_variable_file()
    setup_requirements()
    setup_frontend()
else:
    print("Invalid input. Start again.")
    sys.exit(1)

create_environment_variable_file()

from dotenv import load_dotenv

load_dotenv()


# Function to run a command in a separate thread and print its output
def run_process(command, cwd=None, ready_future=None, ready_signal=None):
    print(os.getcwd())
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def check_ready():
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # Print the server output in real-time
            if ready_signal and ready_signal in line and not ready_future.done():
                ready_future.set_result(True)  # Indicate that the server is ready
        process.stdout.close()

    threading.Thread(target=check_ready).start()
    print(os.getcwd())
    return process


# Function to terminate all running processes and exit
def terminate_processes(processes):
    for process in processes:
        if process.poll() is None:  # If the process is still running
            process.terminate()  # Terminate the process
    sys.exit("Exiting application.")


# Futures to indicate server readiness
backend_ready = Future()
frontend_ready = Future()

# Start the backend server and wait for it to be ready
backend_process = run_process(
    ['python', './server/app.py'],
    ready_future=backend_ready,
    ready_signal='Running on http://127.0.0.1:5000'  # Adjust this to the actual signal from your server output
)

# Start the frontend server and wait for it to be ready
frontend_process = run_process(
    ['yarn', 'run', 'dev'],
    cwd='aichatbot-nuxt',
    ready_future=frontend_ready,
    ready_signal='Nuxt DevTools'  # Adjust this to the actual signal from your server output
)

# Start a separate thread to open the browser after both servers are ready
threading.Thread(target=open_browser, args=(backend_ready, frontend_ready)).start()

# Wait for the backend to complete, and if it exits with an error, terminate the frontend
try:
    backend_process.wait()
    if backend_process.returncode != 0:
        terminate_processes([frontend_process])
except KeyboardInterrupt:
    terminate_processes([backend_process, frontend_process])
