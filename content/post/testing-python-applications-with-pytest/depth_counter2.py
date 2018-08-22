from os import getcwd

def get_cwd_depth():
    path = getcwd()
    return path.count("/")
