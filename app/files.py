from os import walk


def get_files():
    mypath = "./history"
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    return files