from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine
from alembic import context

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from app.core.config import get_settings
from app.core.database import Base
from app.models import models

config = context.config
fileConfig(config.config_file_name)
settings = get_settings()
db_url = settings.alembic_database_url or settings.database_url
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline():
    context.configure(url=db_url, target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(db_url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
