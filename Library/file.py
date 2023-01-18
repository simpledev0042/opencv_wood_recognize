import os

def getFileList( dirPath ) :
    res = []
    for path in os.listdir(dirPath):
        # check if current path is a file
        if os.path.isfile(os.path.join(dirPath, path)):
            res.append(os.path.abspath(dirPath + "/" + path))
    return res