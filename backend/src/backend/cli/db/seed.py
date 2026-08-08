# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ db: seed database                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from __future__ import annotations

import click

from backend.extensions import db
from backend.models import AuditLog, User
from datetime import datetime
from flask.cli import with_appcontext


def seed_admin() -> bool:
    admin = User.query.filter_by(username="admin").first()
    if admin:
        return False
    admin = User(
        username="admin",
        email="admin@ds.study.iitm.ac.in",
        role="admin",
        status="approved",
        is_blacklisted=False,
        created_at=datetime.now(),
    )
    admin.set_password("admin")
    db.session.add(admin)
    db.session.flush()
    db.session.add(
        AuditLog.log(
            action="system_init",
            user_id=admin.id,
            entity_type="user",
            entity_id=admin.id,
            details="admin account created during database seeding.",
        )
    )
    db.session.commit()
    return True


@click.command("seed", help="seed the database with initial data (default admin)")
@with_appcontext
def seed_db() -> None:
    created = seed_admin()
    if created:
        click.echo(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ CREDENTIALS: CREATED                                                                             ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ EMAIL    : admin@ds.study.iitm.ac.in                                                             │
    │ PASSWORD : admin                                                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
            """)
    else:
        click.echo(f"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ CREDENTIALS: EXISTED                                                                             ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ EMAIL    : admin@ds.study.iitm.ac.in                                                             │
    │ PASSWORD : admin                                                                                 │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
            """)
