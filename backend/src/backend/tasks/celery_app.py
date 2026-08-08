# ╭──────────────────────────────────────────────────────────────────────────────────────────────────╮
# │ tasks: celery app                                                                                │
# ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

from app import create_app
from backend.extensions import celery as celery_ext
from backend.lib import make_celery

app = create_app()
celery = make_celery(app, celery_ext)

if __name__ == "__main__":
    celery.start()
