import os


def normalize_path(path):
    return os.path.normpath(os.path.expanduser(path.strip()))
