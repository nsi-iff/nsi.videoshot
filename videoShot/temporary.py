import os
import tempfile
import shutil


class Temporary(object):

    
    def createDirectory(self):
        tempdir = tempfile.mkdtemp(prefix="temporaryVideoDirectory")
        return tempdir
  
    def removeDirectory(self, tempdir):
        shutil.rmtree(tempdir)
