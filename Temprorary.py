import os
from collections import namedtuple
import eel

def system_drive():
    return os.getenv("SystemDrive")

def system_temp():
    return os.getenv("LOCALAPPDATA")

dir_name = "pyeeltube"
dir_temp = os.path.join(system_temp(), "temp")

@eel.expose
def system_gettemp():
    with os.scandir(dir_temp) as _temp:
        dir_found = False
        for temp in _temp:
            if temp.is_dir() and temp.name.lower() == dir_name:
                dir_found = True
                break
        if dir_found != True:
            os.mkdir(dir_temp, dir_name)
            print(f"{dir_name} is created.")
    return os.path.join(dir_temp, dir_name)

@eel.expose
def temp_scandir():
    prototype = namedtuple("temp_scandir", ['datafiles', 'datapath'])
    with os.scandir(system_gettemp()) as _temp:
        datafiles = []
        datapath = []
        for temp in _temp:
            if temp.is_file():
                datafiles.append(temp.name)
                datapath.append(temp.path)
    return prototype(datafiles, datapath)