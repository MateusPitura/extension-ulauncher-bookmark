import os

def get_preferences_path():
    basename = os.path.basename(os.path.dirname(__file__))
    print(f"🌠 basename: {basename}")
    return os.path.expanduser(f'~/.config/ulauncher/{basename}')