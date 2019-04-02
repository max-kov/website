import os

def get_cwd_depth():
    path = os.getcwd()
    return path.count("/")
