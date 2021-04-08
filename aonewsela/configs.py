from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    mnt = Path('/media')
    ludwig_data = mnt / 'ludwig_data'  # path to location of shared drive, mounted on local machine
