# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ db: init                                                                                         ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from flask.cli import AppGroup

from .drop import drop_db
from .init import init_db
from .seed import seed_db

db_cli = AppGroup("db", help="database commands")

db_cli.add_command(drop_db)
db_cli.add_command(init_db)
db_cli.add_command(seed_db)

__all__ = ["db_cli", "drop_db", "init_db", "seed_db"]
