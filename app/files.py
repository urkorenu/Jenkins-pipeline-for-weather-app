from os import walk


def get_files() -> list:
    mypath = "./history"
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break
    return files
