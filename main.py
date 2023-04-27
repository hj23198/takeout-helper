import shutil
import secret
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import random
import time
import json
import logging


def getDoccumentTypeAmountKeyPressesNeeded(url):
    if "docs.google.com/document/d/" in url:
        return 6, ".docx"
    elif "docs.google.com/spreadsheets/d/" in url:
        return 7,  ".xlsx"
    elif "docs.google.com/presentation/d/" in url:
        return 7, ".pptx"
    else:
        return False, False

if not os.path.exists(secret.DESTPATH):
    os.mkdir(secret.DESTPATH)
    os.mkdir(os.path.join(secret.DESTPATH, "Downloads"))
    shutil.copytree(secret.SRCPATH, os.path.join(secret.DESTPATH, "files"))
    with open(os.path.join(secret.DESTPATH, "README.txt"), 'w') as f:
        f.write("The copied files are located in the /file directory. The .json files in this directory are used to keep track of which files have already been downloaded. If you wish to transfer more files in the future, DO NOT modify the file structure. Instead, copy the /files directory and move it elsewhere.")

if not os.path.exists(os.path.join(secret.DESTPATH, "filequeue.json")):
    with open(os.path.join(secret.DESTPATH, "filequeue.json"), 'w') as f:
        fstructure = {}
        pathstack = [os.path.join(secret.DESTPATH, "files")]
        htmlstack = []
        while True:
            if pathstack == []:
                break
            currentpath = pathstack.pop()
            for filename in os.listdir(currentpath):
                if os.path.isdir(os.path.join(currentpath, filename)):
                    pathstack.append(os.path.join(currentpath, filename))
                elif filename.endswith(".html"):
                    htmlstack.append(os.path.join(currentpath, filename))
        json.dump(htmlstack, f)
else:
    with open(os.path.join(secret.DESTPATH,"filequeue.json"), 'r') as f:
        htmlstack = json.load(f)
    with open(os.path.join(secret.DESTPATH, "downloadedfiles.json"), 'r') as f:
        downloaded_files = json.load(f)

#DRIVER IS HERE IF YOU ARE LOOKING TO CHANGE IT
driver = webdriver.Firefox()
logging.basicConfig(filename=os.path.join(secret.DESTPATH, "missing_files.log"), level="WARNING")

#login to Google
driver.get("file://" +os.path.join(os.getcwd(),  'loginmsg.html'))
original_handle = driver.current_window_handle
input("Follow the instructions in the browser window. When you are done, press enter.")

#switch default download location
driver.switch_to.window(original_handle)
driver.switch_to.new_window('tab')
driver.get("about:preferences#searchResults")
time.sleep(1)
ActionChains(driver).send_keys("Downloads").perform()
driver.switch_to.window(original_handle)
with open("settingsmsg.html", "w") as f:
    f.seek(0)
    path = os.path.join(secret.DESTPATH, "Downloads")
    f.write(f"Please open the new tab in your browser window and set to default download location to {path}. Press enter when done.")
driver.get("file://" +os.path.join(os.getcwd(),  'settingsmsg.html'))
input("Follow the instructions in the browser window. When you are done, press enter.")
driver.switch_to.window(original_handle)


while True:
    time.sleep(2+random.random())
    fpath = htmlstack.pop()
    downloaded_files.append(fpath)

    current_file_list = os.listdir(os.path.join(secret.DESTPATH, "Downloads"))
    current_file_list = [f for f in current_file_list if not f.startswith(".")]

    with open(fpath, 'r') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
    anchor = soup.find_all('a', href=True)

    if len(anchor) != 1:
        continue

    url = anchor[0]['href']
    driver.get(url)
    time.sleep(random.random() + 1)
    url = driver.current_url
    amountKeypress, extension = getDoccumentTypeAmountKeyPressesNeeded(url)

    if amountKeypress == False:
        logging.warning(f"Unknown filetype. The following url will NOT be automatically downloaded: {url}")
        with open(os.path.join(secret.DESTPATH, "filequeue.json"), 'w') as f:
            json.dump(htmlstack, f)
        continue
    else: 
        time.sleep(random.random() + 1)
        element = driver.find_element(By.XPATH, '//*[@id="docs-file-menu"]')
        element.click()
        for i in range(amountKeypress):
            time.sleep(random.random()+0.5)     
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()

        ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
        time.sleep(random.random()+1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()

    while True:
        files = os.listdir(os.path.join(secret.DESTPATH, "Downloads"))
        files = [os.path.join(os.path.join(secret.DESTPATH, "Downloads"),  f) for f in files if "." in f and not f.startswith(".")]
        if len(files) == 0:
            time.sleep(1)
            continue
        newest_file = max(files, key=os.path.getctime)
        break

    save_name = fpath[0:-5] + extension

    shutil.copy(newest_file, save_name)
    print(f"File saved to {save_name}")
    os.remove(newest_file)
    os.remove(fpath)

    with open(os.path.join(secret.DESTPATH,"filequeue.json"), 'w') as f:
        json.dump(htmlstack, f)

    with open(os.path.join(secret.DESTPATH,"downloadedfiles.json"), 'w') as f:
        json.dump(downloaded_files, f)





