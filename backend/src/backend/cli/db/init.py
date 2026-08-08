# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ db: init database                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

import click

from backend.extensions import db
from flask.cli import with_appcontext


@click.command("init", help="create database tables")
@with_appcontext
def init_db() -> None:
    inspector = db.inspect(db.engine)

    if inspector.get_table_names():
        click.echo(f"""
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ DATABASE TABLES ALREADY EXISTS                                                                   ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        """)
        return

    db.create_all()
    click.echo(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ DATABASE TABLES CREATED SUCCESSFULLY                                                             ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """)
