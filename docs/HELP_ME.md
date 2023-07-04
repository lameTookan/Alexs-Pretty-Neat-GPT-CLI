
# HELP_ME.md - Beginners Guide to Setting Up This  Project

Welcome! If you have never set up a Python project before, this guide will walk you through the process of setting up this project on your computer, in detail.

## Step 1: Installing Python and Pip

Before we begin, it's important to ensure Python and Pip are both installed on your computer.

### Windows

1. Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/). Get the latest version.

2. Run the installer. During the installation process, make sure to check the box labeled "Add Python to PATH" before clicking "Install Now." This option ensures that Python and Pip (which is included with Python) are accessible from the command line in any directory.

**Note:** The latest versions of Python come with Pip pre-installed. If for some reason Pip is not installed, you can add it later by following these steps:

1. Download get-pip.py from [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py).
2. Open a command prompt and navigate to the location where you downloaded get-pip.py.
3. Run the command `python get-pip.py`.

### Mac/Linux

Python usually comes preinstalled on most Mac/Linux systems. To check if it's installed, open a Terminal window and type `python --version`. If you see a version number in the response, Python is installed.

However, some older systems might not have Pip installed by default. Here's how to install it:

1. If Python 2.7 or later is not installed: Visit [https://www.python.org/downloads/](https://www.python.org/downloads/) and download the latest version. Follow the instructions on the Python website to install Python on your machine.

2. To check if Pip is installed, type `pip --version` or `pip3 --version` in Terminal. If you see a version number, Pip is installed.

3. If Pip is not installed, you can add it with the following command in Terminal: `sudo easy_install pip` for Python 2, or `sudo apt-get install python3-pip` for Python 3.

**Note:** You may need to enter your password for the sudo commands to run.

Double check that Python is installed by running `python --version` in Terminal. If you get a version number, you're good to go.

## Step 2: Cloning the Repository

You have two options for downloading the project files:

1. Through github

- On the project repository page, click the green "Code" button and select "Download ZIP" Extract the ZIP file to your desired location, and make a note of the path to the project folder.

2. Through git
    - Install git from [https://git-scm.com/downloads](https://git-scm.com/downloads)
    - Open your terminal and navigate to the directory where you want to download the project files.
    - Run `git clone https://github.com/lameTookan/Alexs-Pretty-Neat-GPT-CLI` to download the project files.
    - Again, make a note of the path to the project folder.

Use `cd` to navigate to the project folder in your terminal.

## Step 3: Setting Up a Virtual Environment

A virtual environment (venv) keeps the dependencies required by different projects separate by creating isolated Python environments for them.
Install venv by running the following command in your terminal:

```bash
pip install virtualenv
```

### Windows/Mac/Linux

1. Open your terminal.
2. Navigate to your project directory (where you want your new project to be located).
3. Run `python -m venv env` to create a new virtual environment in a folder named `env`.

## Step 4: Activating the Virtual Environment

### Windows

Run `.\env\Scripts\activate`

### Mac/Linux

Run `source env/bin/activate`

You'll know it worked if `(env)` appears at the start of your terminal line.

## Step 5: Installing Requirements

Most Python projects will include a `requirements.txt` file which lists all of the package dependencies. Install these using pip.

Run `pip install -r requirements.txt`

## Step 6: Configuring the .env File

1. Open the `.env.example` file in a text editor.
2. Replace `YOUR_API_KEY_HERE` with your OpenAI API key.
3. If you do not have access to GPT-4, change the DEFAULT_MODEL to `gpt-3` and the DEFAULT_TEMPLATE to `gpt-3_default`.
    - Check out template_directory.md for a list of available templates.
    - If you want to make your own check out `template_documentation.md` in the `docs` folder.(the same folder as this file)
4. Save the file as `.env` in the same directory.

## Step 7: Running the Program

In your terminal, run `python main.py` to start the program.

## Optional: Making Bash/Shell Scripts for Easy Start Up

### Windows

Create a new file with the `.bat` extension. Add the following lines to it:

```bat
@echo off
cd path_to_your_project
.\env\Scripts\activate
python main.py
```

Replace `path_to_your_project` with the full path to your project directory.

### Mac/Linux

Create a new file with the `.sh` extension. Add the following lines to it:

```bash
#!/bin/bash
cd path_to_your_project
source env/bin/activate
python main.py
```

Replace `path_to_your_project` with the full path to your project directory.

Make the script executable by running `chmod +x script_name.sh`.

---

Congratulations! You have successfully set up this project on your computer. If you have any questions, feel free to reach out to me on github or open up an issue! Do not be afraid to ask questions, I am happy to help.
