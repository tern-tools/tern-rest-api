#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

build-dev:
	docker-compose build --force-rm tern-rest-api

serve-dev: build-dev
	docker-compose up --remove-orphans

tests: build-dev
	docker-compose run --rm --volume=$(PWD):/opt/tern-rest-api --entrypoint="/bin/sh" tern-rest-api -c 'pip install tox && tox'

stop:
	docker-compose down -v

update-requirements:
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

doc:
	python -c "import app; app.export_swagger_json('docs/swagger.json')"
