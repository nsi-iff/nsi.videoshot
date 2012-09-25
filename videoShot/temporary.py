import os
import tempfile
import shutil


class Temporary(object):

    
    def createDirectory(self):
        return tempfile.mkdtemp(prefix="temporaryVideoDirectory")
  
    def removeDirectory(self, tempdir):
        shutil.rmtree(tempdir)
