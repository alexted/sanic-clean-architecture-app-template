# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Authors

{{ cookiecutter.app_developer }}

## Implementation language

Python {{ cookiecutter.app_lang_version }}

## Deployment environment

Kubernetes

## Documentation

TODO

## Interaction with 3rd party services

TODO

## Scalability

Scalability is done by `Kubernetes` tools, by adding additional pods.
It is possible to scale by `granian`, by adding additional workers.

## Dependencies

pre-requisites:

```bash
$ poetry new {{ cookiecutter.project_name }} && cd $_        // create a project virtual environment
```

Install the necessary packages:

```bash
({{ cookiecutter.project_name }})$ poetry install                // install all project interceptors
({{ cookiecutter.project_name }})$ poetry install --only main    // install only main project interceptors
```

**Important**:
before running in a container, be sure to execute the ``poetry install'' command,
command to generate poetry.lock - this is the file from which information about dependencies is to be taken when
building the image.
You must also add this file to the git index.

## Startup inside Docker

```bash
$ docker compose up
```

## Set pre-commit hook

```bash
$ pre-commit install
```

## Linter

```bash
$ python -m ruff format && python -m ruff check --fix --unsafe-fixes
```

## Run tests

```bash
$ python -m pytest -vvs
```

## Environment variables

These are the environment variables that you can set for the app to configure it and their default values:

#### `ENVIRONMENT`

String value which defines the runtime environment in which the application runs.

Can have the following values:

* `LOCAL`  *default*
* `TEST`
* `STAGE`
* `PROD`

#### `APP_NAME`

The string variable defining the service name.

By default: `{{ cookiecutter.project_name }}`

### Logging

#### `LOG_LEVEL`

String value which defines the logging severity.

Can have the following values:

* `CRITICAL`
* `ERROR`
* `WARNING`
* `INFO`  *default*
* `DEBUG`

#### `SENTRY_URL`

The url that defines address of the Sentry service.

By default, it's not set.
{% if cookiecutter.use_jwt|lower == 'y' %}
### IdP

#### `IDP_URL`

The url of the Identity and Access Management (IDP) service.

By default, it's not set.

#### `IDP_PUBLIC_KEY`

The public key of the Identity and Access Management (IdP) service.

By default, it's not set.

#### `IDP_CLIENT_SECRET`

The credentials secret of the client (service).

By default, it's not set.
{% endif -%}
{% if cookiecutter.use_postgresql|lower == 'y' or cookiecutter.use_alembic|lower == 'y' %}
### Databases, MessageBrokers

#### `POSTGRES_DSN`

The dsn that defines connection string to of the PostgreSQL.

By default, it's not set.

#### `POSTGRES_MAX_CONNECTIONS`

The int value to setting to limit the number of connections (and resources that are consumed by connections) to the
PostgreSQL.

By default, it's `10`.
{% endif -%}
{% if cookiecutter.use_cache|lower == 'y' %}
#### `CACHE_DSN`

The dsn that defines connection string to of the cache server.

By default, it's not set.
{% endif -%}
{% if cookiecutter.use_kafka|lower == 'y' %}
#### `KAFKA_DSN`

The dsn that defines connection string to of the Kafka.

By default, it's not set.
{% endif %}
