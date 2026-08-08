# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ db: drop database                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import click

from backend.extensions import db
from flask.cli import with_appcontext


@click.command("drop", help="drop all the tables in the database")
@click.confirmation_option(prompt="Do you want to drop all the tables in the database? This action is irreversible.")
@with_appcontext
def drop_db() -> None:
    db.drop_all()
    click.echo(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ DATABASE TABLES DROPPED SUCCESSFULLY                                                             ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)
