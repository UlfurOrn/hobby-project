# hobby-project
A hobby project to try out some stuff

## Setup

## Tools

### alembic

[alembic](https://alembic.sqlalchemy.org/en/latest/index.html) is a migration tool for SQLAlchemy.
It can be used to manage and run migrations between various states of the database schema.

Some of the commands that are useful will be detailed here below.

**NOTE:**
The below commands need to be run from a directory containing an `alembic.ini` file, for example `src/pokemon_api`

#### revision

The `revision` command can be used to autogenerate a migration (revision):

```shell
alembic revision --autogenerate -m "My New Database Change"
```

#### upgrade/downgrade

The `upgrade` and `downgrade` commands can be used to migrate the database to various states (revisions):

```shell
alembic upgrade +1  # Upgrade the database by one revision
alembic downgrade -1  # Downgrade the database by one revision

alembic upgrade abcdef123456  # Upgrade the database to a specific revision
alembic downgrade abcdef123456  # Downgrade the database to a specific revision

alembic upgrade head  # Upgrade the database to the most recent revision
alembic downgrade base  # Downgrade the database to before the first revision (essentially into the state before alembic was introduced)
```

#### current

The `current` command can be used to check the current version (revision) of the database:

```shell
alembic current
```

#### history

The `history` command can be used to list all versions (revisions) of the database:

```shell
alembic history
```

---

### pre-commit

[pre-commit](https://pre-commit.com/) is a tool for managing git hooks.
In this project it is used to run various tooling against the codebase to maintain good Code Quality.

The hooks for a given project are defined in the `.pre-commit-config.yaml` file.

Some of the commands that are useful will be detailed here below.

#### install

The `install` command can be used to install the git hooks for the project:

```shell
pre-commit install
```

This is only required once for a project, or sometimes when a new hook is added.


#### run

The `run` command can be used to run a single or multiple hooks against the repository:

```shell
pre-commit run ruff  # Executes the `ruff` hook against the codebase

pre-commit run -a  # Executes every hook defined for the project against the codebase
```
