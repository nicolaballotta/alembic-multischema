from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/test_multi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'sslmode': "allow"},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

Base = declarative_base(metadata=MetaData(schema="core", naming_convention=convention))
AppBase = declarative_base(metadata=MetaData(schema="app", naming_convention=convention))
