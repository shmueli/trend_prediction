import helpers.constants as constants
import os

def get_times():
    filenames = os.listdir(constants.GRAPHS_FOLDER_NAME)
    filenames.sort()
    return filenames;
