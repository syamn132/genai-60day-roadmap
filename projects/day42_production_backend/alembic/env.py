
from logging.config import fileConfig

from alembic import context

from app.db.session import engine
from app.db.models import Base


# Alembic configuration object
config = context.config


# Configure Alembic logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Our SQLAlchemy table definitions
target_metadata = Base.metadata


# ---------------------------------------
# OFFLINE MIGRATIONS
# ---------------------------------------

def run_migrations_offline():

    database_url = engine.url.render_as_string(
        hide_password=False
    )

    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------
# ONLINE MIGRATIONS
# ---------------------------------------

def run_migrations_online():

    with engine.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------
# CHOOSE EXECUTION MODE
# ---------------------------------------

if context.is_offline_mode():
    run_migrations_offline()

else:
    run_migrations_online()
