

class DataFile:
    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename

    def getFullName(self):
        return self.getDir() + '/' + self.getFilename()

    def getFilename(self):
        return self.filename

    def getDir(self):
        return self.dir
