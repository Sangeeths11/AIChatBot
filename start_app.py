import base64
import subprocess
import sys
import os
import threading
from installRequiredments import setup_requirements
from Setup import setup_frontend, open_browser
from concurrent.futures import Future


def create_environment_variable_file():
    """
    Creates an environment variable file if it does not exist.

    Args:
      None

    Returns:
      None

    Side Effects:
      Creates a file named '.env' in the current working directory.

    Notes:
      The file contains credentials parsed from a file named 'env-cred'.

    Examples:
      >>> create_environment_variable_file()
      None
    """
    # Create the environment variable file if it doesn't exist
    if not os.path.exists('.env'):
        with open('env-cred', 'r') as creds_file:
            creds = creds_file.read()
        decoded_creds = base64.b64decode(creds).decode('utf-8')
        # Parse the JSON credentials
        # Write the credentials to a file
        with open('.env', 'w') as env_file:
            env_file.write(decoded_creds)


def setup():
    """
    Prompts the user to install dependencies and packages if necessary.

    Args:
      None

    Returns:
      None

    Side Effects:
      Installs dependencies and packages if the user agrees.

    Notes:
      If the user agrees, the function will call 'setup_requirements' and 'setup_frontend'.

    Examples:
      >>> setup()
      If this is the first you use this project, we'll need to install some dependencies and packages.
      Shall we proceed?
      If you already installed everything just continue with 'n'.
      Proceed? y / n: y
    """
    r = input("""If this is the first you use this project, we'll need to install some dependencies and packages.
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
        r2 = input("Do you want to setup the frontend? y / n: ")
        if r2.lower() == 'y':
            setup_frontend()
        else:
            print("Okay, let's start the Application.")
    else:
        print("Invalid input. Start again.")
        sys.exit(1)

start = input("""Welcome to BrainWaive.
Do you want to start the application (y) or do you need to setup the Project (n): """)
if start.lower == 'n':
    setup()

create_environment_variable_file()

from dotenv import load_dotenv

load_dotenv()


# Function to run a command in a separate thread and print its output
def run_process(command, shell=True, ready_future=None, ready_signal=None):
    """
    Runs a command in a separate thread and prints its output.

    Args:
      command (list): The command to run.
      shell (bool): Whether to run the command in a shell.
      ready_future (Future): A future to indicate server readiness.
      ready_signal (str): A signal to indicate server readiness.

    Returns:
      subprocess.Popen: The process object.

    Side Effects:
      Prints the server output in real-time.

    Notes:
      If the ready_future and ready_signal are provided, the function will set the future to indicate server readiness when the signal is detected.

    Examples:
      >>> run_process(['python', './server/app.py'], shell=True, ready_future=backend_ready, ready_signal='Running on http://127.0.0.1:5000')
      <subprocess.Popen object at 0x7f8f9f9f9f90>
    """
    # print(os.getcwd())
    process = subprocess.Popen(
        command,
        shell=shell,  # Necessary for commands like 'cd aichatbot-nuxt && yarn run dev'
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8'
    )

    def check_ready():
        """
    Checks if the server is ready.

    Args:
      process (subprocess.Popen): The process object.
      ready_future (Future): A future to indicate server readiness.
      ready_signal (str): A signal to indicate server readiness.

    Returns:
      None

    Side Effects:
      Prints the server output in real-time.
      Sets the future to indicate server readiness when the signal is detected.

    Notes:
      This function is called by 'run_process'.

    Examples:
      >>> check_ready(backend_process, backend_ready, 'Running on http://127.0.0.1:5000')
      None
    """
        try:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')  # Print the server output in real-time
                if ready_signal and ready_signal in line and not ready_future.done():
                    ready_future.set_result(True)  # Indicate that the server is ready
        except:
            print("couldnt decode character probably :D")
        finally:
            process.stdout.close()

    threading.Thread(target=check_ready).start()
    return process


# Function to terminate all running processes and exit
def terminate_processes(processes):
    """
    Terminates all running processes and exits.

    Args:
      processes (list): A list of process objects.

    Returns:
      None

    Side Effects:
      Terminates all running processes.
      Exits the application.

    Notes:
      This function is called when the user presses Ctrl+C.

    Examples:
      >>> terminate_processes([backend_process, frontend_process])
      Exiting application.
    """
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
    shell=True if os.name == 'nt' else False,  # True for Windows, False for Unix/Posix
    ready_future=backend_ready,
    ready_signal='Running on http://127.0.0.1:5000'  # Adjust this to the actual signal from your server output
)

# Start the frontend server and wait for it to be ready
frontend_process = run_process(
    'cd aichatbot-nuxt && yarn run dev',
    shell=True,
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
