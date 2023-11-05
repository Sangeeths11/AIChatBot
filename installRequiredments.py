import os
import shutil
import subprocess
import re
import sys
import time


def check_conda():
    """Check if Conda is installed."""
    try:
        subprocess.check_output(['conda', '--version'], stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_conda_environment_from_file(file_path, env_name):
    """Create a new Conda environment from a .yml file."""
    try:
        # ckeck if name of environment is already taken
        env_name_list = subprocess.check_output(['conda', 'env', 'list'], stderr=subprocess.STDOUT).decode().split('\n')
        env_name_list = [env.split()[0].lower() for env in env_name_list if len(env) > 1]
        print(env_name_list)
        if env_name.lower() in env_name_list:
            subprocess.check_call(['conda', 'env', 'update', '-f', file_path, '--name', env_name])
            print(f"Conda environment ({env_name}) updated from '{file_path}'.")
        else:
            subprocess.check_call(['conda', 'env', 'create', '-f', file_path])
            print(f"Conda environment ({env_name}) created from '{file_path}'.")
    except subprocess.CalledProcessError as e:
        print("An error occurred while creating the Conda environment from the .yml file.")
        print(e.output.decode())

def get_conda_env_name():
    return os.environ.get('CONDA_DEFAULT_ENV', None)


def create_conda_env(file_path='environment.yml'):

    current_env_name = get_conda_env_name()
    if current_env_name is not None:
        active_env_name = current_env_name
        print(f'The currently activated Conda environment is: {current_env_name}')
    else:
        print('No Conda environment is currently activated.')
        active_env_name = 'base'
    # Read the .yml file
    with open(file_path, 'r') as file:
        env_yml = file.read()
    # Use regular expression to find the name
    match = re.search(r'^name:\s*(\S+)', env_yml, flags=re.MULTILINE)
    if match:
        file_env_name = match.group(1)  # This is the environment name
    else:
        raise ValueError("Environment name not found in the .yml file.")

    r = input(f'Would you like to use your active conda environment "{active_env_name}" (y),\nCreate the new environment named "{file_env_name}" (n),\nor Create a new environment with the name of your choosing (input your name)? [y] / [n] / [new_env]: ')
    if r.lower() == 'y':
        env_yml = re.sub(r'^name: .+$', f'name: {active_env_name}', env_yml, flags=re.MULTILINE)
        env_name = active_env_name
    elif (r.lower() != 'n') and (r.lower() != 'y') and (r != ''):
        new_env_name = r
        # Use regular expression to replace the name
        env_yml = re.sub(r'^name: .+$', f'name: {new_env_name}', env_yml, flags=re.MULTILINE)
        env_name = new_env_name
        # Write the changes back to a new .yml file
        with open(file_path, 'w') as file:
            file.write(env_yml)
    elif r.lower() == 'n' or r.lower() == 'y':
        env_name = file_env_name
    else:
        raise ValueError(f'Input "{r}" is invalid.')
    # Write the changes back to a new .yml file
    with open(file_path, 'w') as file:
        file.write(env_yml)
    create_conda_environment_from_file(file_path, env_name)


def install_with_pip():
    """Install packages using pip."""
    try:
        subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Packages installed using pip.")
        time.sleep(5)
    except subprocess.CalledProcessError as e:
        print("An error occurred while installing packages with pip.")
        print(e.output.decode())


def setup_requirements():
    # 1. Check if Node.js is installed
    if not shutil.which("node"):
        print("Node.js is not installed. Please install it from https://nodejs.org/en/download/ and try again.")
        sys.exit(1)
    if check_conda():
        print("Conda is available. Will attempt to create environment from .yml file.")
        r = input("Continue with conda (y) or pip (n)? [y] / [n]: ")
        if r.lower() == 'y':
            create_conda_env()
        elif r.lower() == 'n':
            install_with_pip()
        else:
            print("Invalid input. Start again.")
            sys.exit(1)
    else:
        print("Conda is not available. Falling back to pip for package installation.")
        install_with_pip()
