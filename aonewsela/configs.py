from pathlib import Path


class Dirs:
    src = Path(__file__).parent
    root = src.parent
    ludwig_data = '/media/ludwig_data'  # path to location of shared drive, mounted on local machine
