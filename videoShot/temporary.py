import os
import tempfile
import shutil


class Temporary(object):

    
    def createDirectory(self):
        self.tempdir = tempfile.mkdtemp(prefix="temporaryVideoDirectory")
        return self.tempdir
  
    def removeDirectory(self):
        os.remove(self.filePath)
        os.removedirs(self.tempdir)
