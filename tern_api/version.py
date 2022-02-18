#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from tern.utils.general import VersionInfo

from tern_api.__version__ import version
from tern_api.utils import TernAPIResponse


def get_version() -> TernAPIResponse:
    """Returns the Tern and API version

    :return: Tern API Response
    :rtype: ``TernAPIResponse``
    """

    data = {"tern": VersionInfo("tern").version_string(), "api": version}

    return TernAPIResponse(data=data)
