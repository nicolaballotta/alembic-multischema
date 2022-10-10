# Alembic multi-schema migrations

I created this repository to reproduce an issue I'm experiencing with Alembic and multi-schema migrations. 

This is my current scenario:

* I've some `core` tables that I want to keep separated from other `app` tables and for this reason I'm assigning them 
  different schemas (core and app)
* Tables in the `app` schema should be able to establish relationships with existing tables in the `core` schema (using 
  `backeref`)
* I'm using two separate destinations for Alembic migrations, with two separate env.py scripts that, based on the 
  schema, decide what to migrate using the include_object approach
* The two `env.py` scripts work, and I'm able to create migrations for the two schemas and upgrade them 
* THE PROBLEM: after the first revision/upgrade process, also if I don't touch models and db, ForeignKeys are 
  re-generated everytime I try to create a new revision

***
## Steps to reproduce

* Clone this repository
* run `docker-compose up -d` to start the Postgres database
* run `poetry install` to install dependencies
* enter Poetry shell with `poetry shell`
* run `alembic -c src/multischema/alembic.ini -n core revision --autogenerate`
* run `alembic -c src/multischema/alembic.ini -n app revision --autogenerate`
* run `alembic -c src/multischema/alembic.ini -n core upgrade head`
* run `alembic -c src/multischema/alembic.ini -n app upgrade head`

After these steps, your db should have a `user` table in the `core` schema and a `business` table in the `app` schema.

Now, without touching your db and models, try to create a new revision for the `app` schema:

    alembic -c src/multischema/alembic.ini -n app revision --autogenerate

You should see that Alembic is trying to re-create the ForeignKeys for the `business` table. 