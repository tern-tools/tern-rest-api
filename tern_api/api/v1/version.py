# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from flask_restx import Namespace, Resource, fields

from tern_api.api.v1.common_models import error_model
from tern_api.version import get_version

ns = Namespace("/version", description="Tern REST API Version")


@ns.route("")
class Version(Resource):

    version_data_model = ns.model(
        "version_data_model",
        {
            "tern": fields.String(
                description="Tern current version",
                example="2.9.1",
                required=True,
            ),
            "api": fields.String(
                description="Tern current version",
                example="1.0.0",
                required=True,
            ),
        },
    )
    version_response = ns.model(
        "version_response",
        {
            "data": fields.Nested(version_data_model),
            "error": fields.Nested(error_model),
        },
    )

    @ns.response(200, "OK", version_response)
    @ns.response(400, "Bad request")
    @ns.response(500, "Internal Server Error")
    def get(self):
        """Tern repoort"""

        response = get_version()
        return response.to_response()
