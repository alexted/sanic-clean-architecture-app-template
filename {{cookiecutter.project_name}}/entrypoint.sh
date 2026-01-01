#!/bin/bash

# Set the default ENVIRONMENT if the variable is not set
: "${ENVIRONMENT:=LOCAL}"

# General parameters
APP_NAME="{{cookiecutter.project_name}}"
APP_MODULE="src.service.application:create_app"
HOST="0.0.0.0"
PORT="5000"
INTERFACE="asgi"

# Situational parameters
LOG_LEVEL="info"
WORKERS=${CONCURRENCY:-8}

if [[ $ENVIRONMENT == "LOCAL" ]]; then
    LOG_LEVEL="debug"
    WORKERS=1
fi

{% if cookiecutter.use_alembic|lower == 'y' -%}
echo "Running database migrations..."
exec alembic upgrade head
echo "Starting application..."
{% endif -%}

# Running granian with final parameters
exec granian --interface $INTERFACE \
    --process-name $APP_NAME \
    --host $HOST \
    --port $PORT \
    --log-level $LOG_LEVEL \
    --workers $WORKERS \
    --factory $APP_MODULE
#    --reload \