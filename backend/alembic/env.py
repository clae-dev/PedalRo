import asyncio
import ssl as ssl_module
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings
from app.core.database import Base
from app.models import User, Course, CourseWaypoint, CourseFeedback  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic에서 DATABASE_URL 사용
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def include_name(name, type_, parent_names):
    if type_ == "table" and name == "spatial_ref_sys":
        return False
    return True


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_name=include_name,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connect_args = {}
    if "supabase.com" in settings.DATABASE_URL:
        ssl_context = ssl_module.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl_module.CERT_NONE
        connect_args["ssl"] = ssl_context

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
