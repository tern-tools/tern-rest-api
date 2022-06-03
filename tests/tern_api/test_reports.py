# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import json
import time
from dataclasses import dataclass
from unittest import mock

import pytest

from tern_api import reports
from tern_api.constants import task_status
from tern_api.utils import TernAPIResponse


@dataclass
class FakeSubprocessResult:
    stdout_: bytes
    stderr_: bytes
    returncode_: int

    @property
    def stdout(self):
        return self.stdout_

    @property
    def stderr(self):
        return self.stderr_

    @property
    def returncode(self):
        return self.returncode_


TERN_REPORT = b'{"images": [{"image": "photon", "tag": "3.0"}]}'


class TestReports:
    @mock.patch("tern_api.reports.subprocess.run")
    def test_tern(self, mock_subprocess_run):
        """Test tern report"""

        fake_subprocess_result = FakeSubprocessResult(
            stdout_=b'{"images": [{"image": "photon", "tag": "3.0"}]}',
            stderr_=b"",
            returncode_=0,
        )

        mock_subprocess_run.return_value = fake_subprocess_result
        test_response = reports.tern(
            ["tern", "report", "-i", "phothon:3.0", "-f", "json"]
        )

        assert test_response == json.loads(fake_subprocess_result.stdout_)

    @mock.patch("tern_api.reports.subprocess.run")
    def test_tern_command_failed(self, mock_subprocess_run):
        """Test tern report with a failure running tern command"""

        fake_subprocess_result = FakeSubprocessResult(
            stdout_=b"",
            stderr_=b"Failed to run tern command",
            returncode_=1,
        )

        mock_subprocess_run.return_value = fake_subprocess_result

        with pytest.raises(reports.TernError) as e:
            reports.tern(["tern", "report", "-i", "phothon:3.0", "-f", "json"])

        assert e.value.args[0] == "Failed to run tern command"

    def test_tern_with_invalid_command_type(self):
        """Test tern report with invalid command type for subprocess"""

        with pytest.raises(TypeError) as e:
            reports.tern("tern report -i phothon:3.0 -f json")

        assert e.value.args[0] == "command must be a list"

    @mock.patch("builtins.open", mock.mock_open(read_data=TERN_REPORT))
    def test_tern_report_from_cache(self, test_tern_app, fake_id):
        """Test tern report using cache and cache is available"""
        command = ["tern", "report", "-i", "phothon:3.0", "-f", "json"]

        task_id = fake_id().hex

        with test_tern_app.test_request_context():
            future = reports.tern_report.submit_stored(
                task_id,
                command=command,
                cache=True,
                cache_file="fake_cache_file",
            )

        time.sleep(1)
        assert future._state == "FINISHED"  # futures state
        assert future.done() is True
        assert future.result() == json.loads(TERN_REPORT)

    @mock.patch("builtins.open")
    @mock.patch("tern_api.reports.tern")
    @mock.patch("tern_api.reports.json")
    def test_tern_report_cache_not_available(
        self, mock_json, mock_tern, mock_open, test_tern_app, fake_id
    ):
        """Test tern report using cache and cache is not available"""
        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        command = ["tern", "report", "-i", "phothon:3.0", "-f", "json"]
        task_id = fake_id().hex

        mock_open.side_effect = [
            FileNotFoundError,
            mock.mock_open().return_value,
        ]
        mock_tern.return_value = json.loads(TERN_REPORT)
        mock_json.dump.return_value = None
        with test_tern_app.test_request_context():
            future = reports.tern_report.submit_stored(
                task_id,
                command=command,
                cache=True,
                cache_file="fake_cache_file",
            )

        time.sleep(1)
        assert future._state == "FINISHED"  # futures state
        assert future.done() is True
        assert future.result() == json.loads(TERN_REPORT)

    @mock.patch("tern_api.reports.tern")
    def test_tern_report_no_cache(self, mock_tern, test_tern_app, fake_id):
        """Test tern report without using cache (cache=False)"""
        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        command = ["tern", "report", "-i", "phothon:3.0", "-f", "json"]
        task_id = fake_id().hex

        mock_tern.return_value = json.loads(TERN_REPORT)
        with test_tern_app.test_request_context():
            future = reports.tern_report.submit_stored(
                task_id,
                command=command,
                cache=False,
                cache_file="fake_cache_file",
            )

        time.sleep(1)
        assert future._state == "FINISHED"  # futures state
        assert future.done() is True
        assert future.result() == json.loads(TERN_REPORT)

    @mock.patch("tern_api.reports.os")
    @mock.patch("tern_api.reports.uuid4")
    @mock.patch("tern_api.reports.tern_report")
    def test_request(
        self, mock_os, mock_uuid4, mock_tern_report, test_tern_app, fake_id
    ):
        """Test report request"""

        expected_response = TernAPIResponse(
            data={
                "message": "Request submitted.",
                "id": "fake-id",
                "cache": True,
                "status": task_status.PENDING.value,
                "report": {},
            }
        )

        payload = {
            "registry": "registry_fake_tests",
            "image": "photon",
            "tag": "3.0",
            "cache": True,
        }

        mock_os.return_value = None
        mock_uuid4.return_value.hex = fake_id().hex
        mock_tern_report.submit_stored.return_value = None

        with test_tern_app.app_context():
            test_response = reports.submit(payload=payload)

        assert test_response == expected_response
        assert test_response.status_code == 200

    @mock.patch("tern_api.reports.os")
    @mock.patch("tern_api.reports.uuid4")
    @mock.patch("tern_api.reports.tern_report")
    def test_request_using_different_registry(
        self, mock_os, mock_uuid4, mock_tern_report, test_tern_app, fake_id
    ):
        """Test report request using non-default registry"""

        expected_response = TernAPIResponse(
            data={
                "message": "Request submitted.",
                "id": "fake-id",
                "cache": True,
                "status": task_status.PENDING.value,
                "report": {},
            }
        )

        payload = {
            "registry": "another_registry",
            "image": "photon",
            "tag": "3.0",
            "cache": True,
        }

        mock_os.return_value = None
        mock_uuid4.return_value.hex = fake_id().hex
        mock_tern_report.submit_stored.return_value = None

        with test_tern_app.app_context():
            test_response = reports.submit(payload=payload)

        assert test_response == expected_response

    def test_status(self, test_tern_app, fake_id):
        """Test report status

        The very basic status is a non existent task id (PENDING).
        """

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(id=task_id).to_dict()
        )

        test_result = reports.status(task_id)
        assert test_result == expected_response

    @mock.patch("tern_api.reports.tern_tasks")
    def test_status_task_not_done_running(
        self, mock_tern_tasks, test_tern_app, fake_id
    ):
        """Test report task status is not done and running"""

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(
                id=task_id, status=task_status.RUNNING.value
            ).to_dict()
        )

        # Task didn't finish yet
        mock_tern_tasks.futures.done.return_value = False
        # Task return as running
        mock_tern_tasks.futures._state.return_value = task_status.RUNNING.value

        test_result = reports.status(task_id)
        assert test_result == expected_response

    @mock.patch("tern_api.reports.tern_tasks")
    def test_status_task_not_done_state_not_running(
        self, mock_tern_tasks, test_tern_app, fake_id
    ):
        """Test report task status is not done and state not running"""

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(
                id=task_id, status=task_status.PENDING.value
            ).to_dict()
        )

        # Task didn't finish yet
        mock_tern_tasks.futures.done.return_value = False
        # Task return as running
        mock_tern_tasks.futures._state.return_value = "NOT_RUNNING"

        test_result = reports.status(task_id)
        assert test_result == expected_response

    @mock.patch("tern_api.reports.tern_tasks")
    def test_status_task_success(
        self, mock_tern_tasks, test_tern_app, fake_id
    ):
        """Test report task status is not done and state not running"""

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(
                id=task_id,
                status=task_status.SUCCESS.value,
                report=json.loads(TERN_REPORT),
            ).to_dict()
        )

        # Task didn't finish yet
        mock_tern_tasks.futures.done.return_value = True

        mocked_result = mock.Mock()
        mocked_result.result.return_value = json.loads(TERN_REPORT)
        mock_tern_tasks.futures.pop.return_value = mocked_result

        test_result = reports.status(task_id)
        assert test_result == expected_response

    @mock.patch("tern_api.reports.tern_tasks")
    def test_status_tern_error(self, mock_tern_tasks, test_tern_app, fake_id):
        """Test report task status success but tern error (finished)"""

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(
                id=task_id,
                status=task_status.SUCCESS.value,
            ).to_dict()
        )
        expected_response.errors = {"message": "fake error"}

        # Task raise a handled error from Tern, what means the task
        # is success finished.
        mock_tern_tasks.futures.done.side_effect = reports.TernError(
            "fake error"
        )

        test_result = reports.status(task_id)
        assert test_result == expected_response

    @mock.patch("tern_api.reports.tern_tasks")
    def test_status_task_error(self, mock_tern_tasks, test_tern_app, fake_id):
        """Test report task status failed during the process (unfinished)"""

        # clean test tern tasks
        test_tern_app.config["TERN_TASKS"].futures.pop("fake-id")

        task_id = fake_id().hex
        expected_response = TernAPIResponse(
            reports.DataResponse(
                id=task_id,
                status=task_status.FAILURE.value,
                message="Task could not finish due",
            ).to_dict()
        )
        # Task raise a error, what means the task is didn't finished.
        mock_tern_tasks.futures.done.side_effect = TypeError(
            "wrong type during process"
        )

        test_result = reports.status(task_id)
        assert test_result.status_code == 200
        assert expected_response.data.get("message") in test_result.data.get(
            "message"
        ), test_result.data.get("message")
