import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_PATH = ROOT / 'app'
if APP_PATH.exists():
    sys.path.insert(0, str(APP_PATH))
