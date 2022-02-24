# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from tern_api.version import VersionInfo, version
from tests.utils import RequestDataTest


class TestVersion:
    def test_version(self, api_request):
        expected_response = {
            "api": version,
            "tern": VersionInfo("tern").version_string(),
        }
        test_response = api_request(
            RequestDataTest(
                method="GET", endpoint="/api/v1/version", payload=None
            )
        )
        assert test_response.json.get("data") == expected_response
