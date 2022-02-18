#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from flask_restx import Namespace, fields

api_models_namespace = Namespace("Models")


error_model = api_models_namespace.model(
    "error_model",
    {
        "message": fields.String(
            description="error message",
            example="Failed during the processing.",
        ),
    },
)

async_response_model = api_models_namespace.model(
    "async_response_model",
    {
        "message": fields.String(
            description="Status message",
            requored=True,
            example="Request submitted.",
        ),
        "id": fields.String(
            description="Unique Identification for request",
            required=True,
            example="19f035a711644eab84ef5a38ceb5572e",
        ),
    },
)

image_report_data = api_models_namespace.model(
    "image_report_data",
    {
        "repotag": fields.String(
            descripton="Repository tag",
            example="photon:3.0",
            required=True,
        ),
        "name": fields.String(
            descripton="Image name",
            example="photon",
            required=True,
        ),
        "tag": fields.String(
            descripton="Image tag",
            example="3.0",
            required=True,
        ),
    },
)
image_report_model = api_models_namespace.model(
    "image_report_mode", {"image": fields.Nested(image_report_data)}
)
report_model = api_models_namespace.model(
    "report_mode", {"images": fields.List(fields.Nested(image_report_model))}
)
