import os
from pathlib import Path
from typing import Optional, Dict
from unittest import mock
import json

import pytest

from dynatrace import Dynatrace
from dynatrace.http_client import HttpClient

current_file_path = os.path.dirname(os.path.realpath(__file__))


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data
        self.headers = {}

    def json(self):
        return self.json_data


def local_make_request(self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, method="GET", data=None) -> MockResponse:
    file_name = f'{method}{path.replace("/", "_")}.json'
    file_path = Path(current_file_path, "mock_data", file_name)
    with open(file_path) as f:
        json_data = json.load(f)
        return MockResponse(json_data)


@pytest.fixture(autouse=True)
def dt():
    with mock.patch.object(HttpClient, "make_request", new=local_make_request):
        dt = Dynatrace("mock_tenant", "mock_token")
        yield dt
