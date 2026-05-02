import os


def get_preferences_path(dirname):
    basename = os.path.basename(dirname)
    return os.path.expanduser(f'~/.config/ulauncher/{basename}')
