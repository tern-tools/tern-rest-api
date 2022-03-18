#!/bin/bash

if [[ ${ENVIRONMENT^^} == "DEVELOPMENT" ]]; then
    echo "Starting tern-rest-api in development mode"
    gunicorn --reload -b 0.0.0.0:80 app:tern_app
else
    gunicorn -b 0.0.0.0:80 app:tern_app
fi