#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from flask import request
from flask_restx import Namespace, Resource, fields

from tern_api import reports, tern_app
from tern_api.api.v1.common_models import (
    async_response_model,
    error_model,
    report_model,
)

ns = Namespace("/reports", description="Tern Bill of Materials Report")


@ns.route("")
class Report(Resource):
    report_parameters = ns.model(
        "report_parameters",
        {
            "registry": fields.String(
                description="Registry Server",
                required=False,
                default=tern_app.config["TERN_DEFAULT_REGISTRY"],
                example=tern_app.config["TERN_DEFAULT_REGISTRY"],
            ),
            "image": fields.String(
                description="Image name",
                required=True,
                example="photon",
            ),
            "tag": fields.String(
                description="Image tag",
                required=True,
                example="3.0",
            ),
            "cache": fields.Boolean(
                description="Use cache data if available?",
                required=True,
                example=True,
            ),
        },
    )
    report_response_request = ns.model(
        "report_response_request",
        {
            "data": fields.Nested(async_response_model),
            "error": fields.Nested(error_model),
        },
    )

    @ns.response(200, "OK", report_response_request)
    @ns.expect(report_parameters)
    def post(self):
        """Tern BoM report

        **Note**: This request will be processed assynchronous.
        """
        payload = request.json
        response = reports.request(payload)
        return response.to_response()


@ns.route("/status")
class ReportStatus(Resource):
    report_status_parameters = ns.model(
        "report_status_parameters",
        {
            "id": fields.String(
                description="Unique Identification for request",
                required=False,
                example="19f035a711644eab84ef5a38ceb5572e",
            ),
        },
    )
    data_status_response = ns.model(
        "data_status_response",
        {
            "status": fields.String(
                description="Status of request",
                required=True,
                example="FINISH",
                enum=["UNKNOWN", "FINISH", "RUNNING", "FAIL"],
            ),
            "result": fields.Nested(report_model),
        },
    )
    report_status_response = ns.model(
        "report_status_response",
        {
            "data": fields.Nested(data_status_response),
            "error": fields.Nested(error_model),
        },
    )

    @ns.response(200, "OK", report_status_response)
    @ns.expect(report_status_parameters)
    def post(self):
        """Request Tern BoM report status/result"""

        payload = request.json
        response = reports.status(payload.get("id"))
        return response.to_response()
