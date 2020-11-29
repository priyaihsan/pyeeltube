import os

def cleansing(filename):
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    filename = filename.replace(":", "")
    filename = filename.replace("<", "")
    filename = filename.replace(">", "")
    filename = filename.replace("|", "")
    filename = filename.replace('"', "")
    return filename

def rcleansing(filename):
    path = filename.rsplit("\\", 1)[0]
    filename = filename.rsplit("\\", 1)[1]
    filename = cleansing(filename)
    filename = os.path.join(path, filename)
    return filename