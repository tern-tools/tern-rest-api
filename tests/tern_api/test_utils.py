# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from tern_api.utils import TernAPIResponse


class TestTernAPIResponse:
    def test_ternapi_response(self, test_tern_app):
        """Test ternapi_response() basic functionality"""
        with test_tern_app.app_context():
            response = TernAPIResponse()

            assert response.status_code == 200
            assert response.data == {}
            assert response.errors == {}
            assert response.to_response().status_code == 200
            assert response.to_response().json == {"data": {}}

    def test_to_response_with_data(self, test_tern_app):
        """Test to_response() functionality with data"""

        with test_tern_app.app_context():
            response = TernAPIResponse(
                data={"key": "value"},
            )

            assert response.to_response().status_code == 200
            assert response.to_response().json == {"data": {"key": "value"}}

    def test_to_response_with_errors(self, test_tern_app):
        """Test to_response() with errors"""
        with test_tern_app.app_context():
            response = TernAPIResponse(
                errors={"message": "error"},
            )

            assert response.to_response().status_code == 200
            assert response.to_response().json == {
                "data": {},
                "error": {"message": "error"},
            }

    def test_to_response_not_200(self, test_tern_app):
        """Test bto response when is not 200 HTTP code"""
        with test_tern_app.app_context():
            response = TernAPIResponse(
                errors={"message": "Bad Request"}, status_code=400
            )

            assert response.to_response().status_code == 400
            assert response.to_response().json == {
                "data": {},
                "error": {"message": "Bad Request"},
            }
