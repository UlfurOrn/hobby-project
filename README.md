# hobby-project
A hobby project to try out some stuff

## Setup

## Tools

### Alembic

[alembic](https://alembic.sqlalchemy.org/en/latest/index.html) is a migration tool for SQLAlchemy.
It can be used to manage and run migrations between various states of the database schema.

Some of the commands that are useful will be detailed here below.

**NOTE:**
The below commands need to be run from a directory containing an `alembic.ini` file, for example `src/pokemon_api`

#### Revision

The `revision` command can be used to autogenerate a migration (revision):

```shell
alembic revision --autogenerate -m "My New Database Change"
```

#### Upgrade/Downgrade

The `upgrade` and `downgrade` commands can be used to migrate the database to various states (revisions):

```shell
alembic upgrade +1  # Upgrade the database by one revision
alembic downgrade -1  # Downgrade the database by one revision

alembic upgrade abcdef123456  # Upgrade the database to a specific revision
alembic downgrade abcdef123456  # Downgrade the database to a specific revision

alembic upgrade head  # Upgrade the database to the most recent revision
alembic downgrade base  # Downgrade the database to before the first revision (essentially into the state before alembic was introduced)
```

#### Current

The `current` command can be used to check the current version (revision) of the database:

```shell
alembic current
```

#### History

The `history` command can be used to list all versions (revisions) of the database:

```shell
alembic history
```
