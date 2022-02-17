# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import json
import logging

from flask_restx import Api

from tern_api import __version__, tern_api
from tern_api.api.v1.commom_models import api_models_namespace
from tern_api.api.v1.reports import ns as report_v1
from tern_api.api.v1.version import ns as version_v1

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)


api = Api(
    tern_api,
    version=__version__.version,
    title="Tern REST API",
    description="Tern Project REST API",
)

api.add_namespace(api_models_namespace)
api.add_namespace(version_v1, path="/api/v1/version")
api.add_namespace(report_v1, path="/api/v1/report")


def export_swagger_json(filepath):
    tern_api.config["SERVER_NAME"] = "localhost"
    with tern_api.app_context().__enter__():
        with open(filepath, "w") as f:
            swagger_json = json.dumps(api.__schema__, indent=4)
            f.write(swagger_json)
