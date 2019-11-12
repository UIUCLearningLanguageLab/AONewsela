from pathlib import Path


class Dirs:
    root = Path(__file__).parent.parent
    src = root / 'boysvgirls'
    data = root / 'data'