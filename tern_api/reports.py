#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json
import logging
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional
from uuid import uuid4

from tern_api import tern_app, tern_tasks
from tern_api.constants import task_status
from tern_api.utils import TernAPIResponse


class TernError(Exception):
    """Failure on the Tern execution."""


@dataclass
class DataResponse:
    id: str
    cache: bool = field(default=True)
    message: str = field(default="")
    status: str = field(default=task_status.PENDING.value)
    report: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Returns the DataResponse as a dictionary."""
        return asdict(self)


def tern(command: list) -> Dict[str, Any]:
    """
    Runs the tern CLI using the ``subprocess``.

    Args:
        command: Command line as a list (required by subprocess).

    Returns:
       report as a dictionary (JSON).

    Raises:
        TernError: failure during running the command from tern CLI.
    """
    logging.debug(command)

    tern_cmd = subprocess.run(command, capture_output=True)
    if tern_cmd.stdout:
        json_report = json.loads(tern_cmd.stdout)
        return json_report
    else:
        if tern_cmd.stderr:
            logging.debug(tern_cmd.stderr)

            # Is important to return a specific error if the error comes from
            # tern CLI, it means the task FINISH, for example, invalid image.
            logging.info(tern_cmd.stderr)
            raise TernError(tern_cmd.stderr)


@tern_tasks.job
def tern_report(
    command: list, cache: bool, cache_file: Optional[str]
) -> Dict[str, Any]:
    """
    Tern Report as a task (background) and manages the cache

    Args:
        command: Command line as a list (required by subprocess).
        cache: Use caching
        cache_file: If cache, inform the cache_file

    Return:
        Report as Dictionary
    """

    if cache:
        # If a API user is using the cache, first try to load the cached
        # instead doing a new call to the tern.
        try:
            with open(cache_file, "r") as f:
                report = json.load(f)
            return report
        except FileNotFoundError:
            # call the tern and dump it to the cache
            report = tern(command)
            with open(cache_file, "w") as f:
                json.dump(report, f, indent=2)
    else:
        report = tern(command)

    return report


def request(payload: dict) -> TernAPIResponse:
    """
    Get the Payload from API and prepare to request the report.
    The request will be handled in the background as tern tasks.

    Args:
        payload: API Payload

    Return:
        API Response
    """
    TERN_API_CACHE_DIR = tern_app.config["TERN_API_CACHE_DIR"]
    TERN_DEFAULT_REGISTRY = tern_app.config["TERN_DEFAULT_REGISTRY"]

    task_id = uuid4().hex
    registry = payload.get(
        "registry",
    )
    image = payload.get("image")
    tag = payload.get("tag")
    cache = payload.get("cache", True)
    cache_file_dir = os.path.join(TERN_API_CACHE_DIR, registry, image)
    cache_file = os.path.join(cache_file_dir, f"{tag}.json")

    os.makedirs(cache_file_dir, exist_ok=True)

    report_request_response = DataResponse(id=task_id, cache=cache)
    if registry != TERN_DEFAULT_REGISTRY:
        registry_image_tag = f"{registry}/{image}:{tag}"
    else:
        registry_image_tag = f"{image}:{tag}"

    command = ["tern", "report", "-i", registry_image_tag, "-f", "json"]
    logging.info(command)

    tern_report.submit_stored(
        task_id, command=command, cache=cache, cache_file=cache_file
    )

    report_request_response.message = "Request submitted."
    return TernAPIResponse(report_request_response.to_dict())


def status(task_id: str) -> TernAPIResponse:
    """
    Request to the status/result from the tern tasks.

    The tern tasks can have basically the following status:
    - UNKNOWN: Not known (yet) by the task manager (initial status).
    - RUNNING: Task is running by the task manager.
    - FINISH : Task has fineshed in the task manager.
    - FAIL   : Task has failed before finished.

    Args:
        task_id: the unique task ID
    """
    data_response = DataResponse(id=task_id, status=task_status.UNKNOWN.value)

    try:
        if not tern_tasks.futures.done(task_id):
            status = tern_tasks.futures._state(task_id)
            if status:
                data_response.status = status

            return TernAPIResponse(data_response.to_dict())

        report = tern_tasks.futures.pop(task_id)
        data_response.report = report.result()
        data_response.status = task_status.SUCCESS.value

    # It means the task was finished by the task manager (SUCCESS), but the
    # report has no data and the error is given to the API user.
    except TernError as e:
        data_response.status = task_status.SUCCESS.value
        response = TernAPIResponse(data_response.to_dict())
        response.errors = {"message": str(e)}
        return response

    # Any kind of not expected failure means that the task didn't finished as
    # expected (FAIL).
    except:  # noqa
        data_response.status = task_status.FAILURE.value
        data_response.message = (
            f"Task couln't finish due: {str(sys.exc_info())}"
        )

    return TernAPIResponse(data_response.to_dict())
