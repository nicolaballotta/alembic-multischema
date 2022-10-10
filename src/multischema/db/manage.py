from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlalchemy.schema import CreateSchema


SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/test_multi"


def init_db(engine):
    """Initializes the database."""
    print("Initializing database...")
    if not database_exists(str(SQLALCHEMY_DATABASE_URI)):
        create_database(str(SQLALCHEMY_DATABASE_URI))
    else:
        print("Database already exists.")
    schemas = ["core", "app"]
    for schema in schemas:
        if not engine.dialect.has_schema(engine, schema):
            with engine.connect() as connection:
                connection.execute(CreateSchema(schema))
    conn = engine.connect()
    conn.execute("set search_path to core")


def drop_db():
    """Drops the database."""
    print("Dropping database...")
    if database_exists(str(SQLALCHEMY_DATABASE_URI)):
        drop_database(str(SQLALCHEMY_DATABASE_URI))
    else:
        print("Database does not exist.")
