
# A tool for downloading shared files from Google Takeout 

# Still in development, highly recommened against using at the moment 

Have you ever been in that all too common situation where your school Google acount is about to be deleted?
The easy solution is to use Google takeout, which sends you a copy of all your accounts data. However, this method comes with a drawback. 

For files that are shared with your Google account, they are not actually downloaded. Instead, you are provided a url to the doccument. 
The obvious issue with this is since you no longer have access to your account, you also no longer have access to the shared doccuments.

While it is possible to manually download all of them, with tools such as Google Classroom, you can have hundreds or ever thousands of shared files associated with your school Google account.

This script automatically downloades shared files missing from a Google Takeout folder.  

# Note
This script ONLY copies word doccuments, spreadsheets, and presentations. However, some of these files may fail to download for some reason. 
Details are provided at the end of the "Slowstart" with how to address this issue under "Missing Files".

## Requirments
- Python3
- Firefox
- geckodriver

## Quickstart (for those who have an idea of what they are doing)
- Clone repository
- Ensure you have Firefox and geckodriver installed (or replace the driver in line 38 of main.py)
- pip install -r requirements.txt
- Replace SRCPATH in secret.py with the path to "Takeout/Drive" of your Google Archive
- Replace DESTPATH in secret.py with any desired path (a backup of your Archive is made instead of modifying the original)
- Run main.py 

## Slowstart (for those who have no idea of what they are doing)
# Dependencies
- Open a terminal.
- Type "git --version" and press enter
- If you see a version, your good to go. Otherwise, install git (https://git-scm.com/downloads)
- Type "python --version" and press enter. If you do not see a version, try "python3 --version". If neither of these work, install python3 (https://www.python.org/downloads/)
- If you do not have Firefox, install it (https://www.mozilla.org/en-US/firefox/new/)
- If you do not have geckodriver, install it (https://github.com/mozilla/geckodriver/releases)

# Download 
- Create a folder for the download
- Go back to the terminal and type "cd " followed by the file path to the folder you just created, then press enter. If at any point you close the terminal, this will need to be done again before you continue
- Click on the green "<> Code" button in this github repository. Copy the link to your clipboard
- Go back to the terminal and type "git clone " then paste the link into the terminal. Hit enter. All the this projects files will be copied to the folder. 

# Setting up enviornment 
- Type "python -m venv .venv" and press enter. Then, type "source .venv/bin/activate". You may need to use "python3" instead of "python"
- Type "pip install -r requirments.txt". This installs the librarys the script uses

# Configuration 
- Type "open ." This should open an instance of finder in the project folder.
- Locate "secret.py" and open it in any text editor 
- Replace the file path to the right of "SRCPATH" with that of the "Drive" folder in your Google Takeout, and "DESTPATH" with an empty folder that you want the data copied to. If anything goes wrong, the original Google Takeout folder is completly unmodified 
- Example: 
- SRCPATH = "/Users/username/Desktop/Takeout/Drive"
- DESTPATH = "/Users/username/Desktop/Copy of Drive"

# Running 
- Type "python main.py". "python" might need to be replaced with "python3". This will start the script. If for some reason you want to stop the script, you can press control + c while in the terminal
- At this point a Firefox window should automatically open with a window to more instructions (How fun!). However, those instructions are also detained below

# Operation
- Do not close the automatically opened tab or rearrange tabs. This could cause an issue later.
- Open a new tab and sign in to Google. This allows files shared with you to be accessed. Make sure that you are signing into the Google account associated with the Google Takeout
- Go back to the terminal and press enter. This signals to the script that you are signed in and will start the download process. 
- If something happens and the script crashes, restart it with "python main.py". It will automatically resume its place, but you will need to sign in to Google again 

# Missing Files
Some files will either fail to download, or not be supported by this script. Please check "output.log" (Located in the folder you created at the begining) 
for a list of these files. The log file will provide urls to the missing files, but these will need to be downloaded manually. 






