import os

def ensure_folder(folder_name):
    d = os.path.dirname(folder_name)
    if not os.path.exists(d):
        os.makedirs(d)
