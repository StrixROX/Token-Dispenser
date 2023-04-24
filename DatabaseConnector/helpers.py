import os

def getAbsolutePath(relPath:str):
  return os.path.join(os.path.realpath(__file__), relPath)