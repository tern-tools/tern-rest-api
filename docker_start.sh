#!/bin/bash

if [[ ${ENVIRONMENT^^} == "DEVELOPMENT" ]]; then
    flask run --reload --debugger -h 0.0.0.0 -p 80
else
    gunicorn --workers=1 -b 0.0.0.0:80 app:tern_api
fi