import Style as box
from colorama import *

import os
import eel
import requests
import json
import time
import tkinter as tk
from tkinter import filedialog
from youtubesearchpython import SearchVideos
from datetime import datetime as dt

# operation system color initalized
os.system("")

# global used variable
ds = ""
path = ""

@eel.expose
def hello():
    print("Hello world!")

@eel.expose
def refresh():
    global path
    global ds
    ds = ""
    path = ""
    print(f"{Fore.GREEN}(Listening){Fore.RESET} to {Fore.BLUE}Python{Fore.RESET}")

@eel.expose
def openDir():
    global path
    os.system(f"start {path}")

def pattern_filename(filename):
    filename = filename.replace("/", " - ")
    filename = filename.replace("\\", " - ")
    filename = filename.replace(":", " - ")
    filename = filename.replace("<", " - ")
    filename = filename.replace(">", " - ")
    filename = filename.replace("|", " - ")
    filename = filename.replace('"',"")
    return filename

def search(_title, _offset, _mode, _count):
    return SearchVideos(
        _title,
        offset=_offset,
        mode=_mode,
        max_results=_count
    )

def getThumbnails(ctx):
    ctx = ctx.result()
    data = json.loads(ctx)
    index = 0
    print("\nSearching...")
    for _data in data["search_result"]:
        index = index + 1
        title = _data["title"]
        print(f"[{Fore.BLUE}{index}{Fore.RESET}] {title}")
    print("==Done result==")
    print()
    return data

def getUrlThumbnails(source):
    data = source["search_result"]
    eel.clearObj()

    for idx in data:
        url = idx["thumbnails"][4]
        eel.makeObj(url)

def is_downloadable(url):
    head = requests.head(url, allow_redirects=True)
    header = head.headers
    content_type = header.get("Content-Type")
    if "text" in content_type.lower():
        return False
    if "html" in content_type.lower():
        return False
    return True

def initTitle(title):
    global ds
    ds = getThumbnails(
        search(
            title, 
            1,
            "json",
            15
        )
    )
    getUrlThumbnails(ds)

@eel.expose
def makeObj(title):
    initTitle(title)

@eel.expose
def getUrlFromIndex(idx):
    idx = [(int(x)) for x in idx]
    global ds
    data = ds["search_result"]
    for i in idx:
        url = data[i]["thumbnails"][4]
        eel.download(url)

@eel.expose
def setDirectory():
    global path
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    eel.dialogSwap(True, "")
    path = filedialog.askdirectory()
    while True:
        if len(path) > 0:
            eel.dialogSwap(False, path)
            break
        else:
            eel.dialogSwap(True, "")
            path = filedialog.askdirectory()
    is_pathed()
    eel.getSelectedIndex()
    print("Path set to :", path)
    del root

@eel.expose
def is_pathed():
    global path
    print("catch : ", path)
    if len(path) > 0:
        print("set to true")
        eel.is_pathed(True)
    else:
        eel.is_pathed(False)

def getFileSize(url):
    data = requests.head(url, allow_redirects=True)
    header = data.headers
    size = header["Content-Length"]
    size = round(float(size)/1024, 1)
    return size

@eel.expose
def core_downloadThumbnails(_list):
    global path
    global ds
    data = ds["search_result"]
    _list = ([int(_list) for _list in _list])
    amount = len(_list);
    pathsave = path.replace("/", "\\")
    eel.progressbar()
    eel.btnDownload(True)
    try:
        for idx in _list:
            title = pattern_filename(data[idx]["title"])
            url_thumbnails = data[idx]["thumbnails"][4]
            size = getFileSize(url_thumbnails)
            thumbname = url_thumbnails.rsplit("/", 1)[1]
            print(f"{Fore.BLUE}get :{Fore.RESET}", title)
            r = requests.get(url_thumbnails)
            if is_downloadable(url_thumbnails):
                with open(f"{pathsave}\\{title}_{thumbname}", "wb") as file:
                    print(f"{Fore.GREEN}({size} KB) Downloading : {Fore.RESET}{Fore.BLUE}{title}{Fore.RESET}")
                    file.write(r.content)
                    eel.updateProgressbar(amount)
                    print(f"{box.style(0, 37, 42)}Download Success{box.end()}")
        
        time.sleep(.5)
        eel.btnDownload(False)
        eel.clearChecked()
        eel.progressbar()
        
    except Exception as ex:
        print(f"{box.style(0,37,41)}Error catched.{box.end()}")

    


eel.init("www")
eel.start("App1.html")