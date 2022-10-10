# Alembic multi-schema migrations

I initially created this repository to reproduce an issue I was experiencing with Alembic and multi-schema 
migrations. Then I solved the issue (which was really stupid, a leftover in my code) and decided to keep the repository 
for people who want a working example of Alembic with multi-schema migrations in separated folders. 

## What I wanted to achieve

* I have some `core` tables that I want to keep separated from other `app` tables and for this reason I'm assigning 
  them different schemas (core and app)
* Tables in the `app` schema should be able to establish relationships with existing tables in the `core` schema (using 
  `backeref`)
* I want Alembic migrations for every schema, to be in different locations. So two separate env.py scripts that, 
  based on the schema, decide what to migrate using the include_object approach

  
## Steps to bootstrap the project

* Clone this repository
* run `docker-compose up -d` to start the Postgres database
* run `poetry install` to install dependencies
* enter Poetry shell with `poetry shell`
* run `python src/multischema/create_db_with_schema.py` to create the database and the two schemas
* run `alembic -c src/multischema/alembic.ini -n core revision --autogenerate`
* run `alembic -c src/multischema/alembic.ini -n app revision --autogenerate`
* run `alembic -c src/multischema/alembic.ini -n core upgrade head`
* run `alembic -c src/multischema/alembic.ini -n app upgrade head`

After these steps, your db should have a `user` table in the `core` schema and a `business` table in the `app` schema.