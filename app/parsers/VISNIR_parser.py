import sys
from pathlib import Path

# go up 3 levels: parsers -> app -> backend
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.mDB_connect_to_db import DbConnect
from app.parsers.clean_xlsx import CleanXlsx