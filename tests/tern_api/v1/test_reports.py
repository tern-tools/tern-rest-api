# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from unittest import mock

from tern_api.utils import TernAPIResponse
from tests.utils import RequestDataTest


class TestAPIReports:
    @mock.patch("tern_api.api.v1.reports.submit")
    def test_post_reports(self, mock_reports_submit, api_request):
        expected_response = {
            "data": {
                "message": "Request submitted.",
                "id": "fake-id",
                "cache": True,
            }
        }

        payload = {
            "registry": "registry.hub.docker.com",
            "image": "photon",
            "tag": "3.0",
            "cache": True,
        }

        mock_reports_submit.return_value = TernAPIResponse(expected_response)
        test_response = api_request(
            RequestDataTest(
                method="POST", endpoint="/api/v1/reports", payload=payload
            )
        )
        assert test_response.status_code == 200
        assert test_response.json.get("data") == expected_response

    def test_post_reports_missing_required_payload(self, api_request):
        expected_response = {
            "errors": {
                "cache": "'cache' is a required property",
                "image": "'image' is a required property",
                "tag": "'tag' is a required property",
            },
            "message": "Input payload validation failed",
        }

        test_response = api_request(
            RequestDataTest(
                method="POST", endpoint="/api/v1/reports", payload={}
            )
        )
        assert test_response.status_code == 400
        assert test_response.json == expected_response, test_response.json

    @mock.patch("tern_api.api.v1.reports.status")
    def test_post_reports_status(self, mock_reports_status, api_request):
        expected_response = {
            "data": {
                "cache": True,
                "id": "19f035a711644eab84ef5a38ceb5572e",
                "message": "",
                "report": {},
                "status": "PENDING",
            }
        }

        payload = {
            "id": "fake-id",
        }

        mock_reports_status.return_value = TernAPIResponse(expected_response)

        test_response = api_request(
            RequestDataTest(
                method="POST",
                endpoint="/api/v1/reports/status",
                payload=payload,
            )
        )
        assert test_response.status_code == 200
        assert test_response.json.get("data") == expected_response

    @mock.patch("tern_api.api.v1.reports.status")
    def test_post_reports_status_invalid_payload(
        self, mock_reports_status, api_request
    ):
        expected_response = {
            "errors": {
                "id": "'id' is a required property",
            },
            "message": "Input payload validation failed",
        }

        payload = {}

        mock_reports_status.return_value = TernAPIResponse(expected_response)

        test_response = api_request(
            RequestDataTest(
                method="POST",
                endpoint="/api/v1/reports/status",
                payload=payload,
            )
        )
        assert test_response.status_code == 200
        assert test_response.json.get("data") == expected_response
