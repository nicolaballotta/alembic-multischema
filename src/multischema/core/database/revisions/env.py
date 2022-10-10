from alembic import context
from sqlalchemy import engine_from_config, pool

from multischema.db.base import Base
from multischema.core_models import User

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/test_multi"

config = context.config

config.set_main_option("sqlalchemy.url", str(SQLALCHEMY_DATABASE_URI))

target_metadata = Base.metadata  # noqa


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        if object.schema == "core":
            return True
        elif object.schema == "app":
            return False
        elif name == "core_alembic_version":
            return False
        else:
            return True


def run_migrations_online():
    # don't create empty revisions
    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes found skipping revision creation.")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    print("Migrating JetOS Core tables...")
    with connectable.connect() as connection:
        connection.execute('set search_path to core')
        connection.dialect.default_schema_name = "core"
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
            version_table="core_alembic_version",
            version_table_schma="app",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("Can't run migrations offline")
else:
    run_migrations_online()
