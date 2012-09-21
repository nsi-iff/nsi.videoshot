import os
import tempfile
import shutil


class Temporary(object):

    
    def createDirectory(self):
        self.tempdir = tempfile.mkdtemp(prefix="temporaryVideoDirectory")
        return self.tempdir
  
    def removeDirectory(filePath, tempdir):
        os.remove(filePath)
        os.removedirs(tempdir)
