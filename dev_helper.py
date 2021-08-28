"""
This file can be used during development to automatically generate mock data from the API calls.
Please check CONTRIBUTING.md for details
"""

import hashlib
import json
import logging
import os
from pathlib import Path

import wrapt

from dynatrace import Dynatrace
from dynatrace.utils import slugify


@wrapt.patch_function_wrapper("dynatrace.http_client", "HttpClient.make_request")
def dump_to_json(wrapped, instance, args, kwargs):
    r = wrapped(*args, **kwargs)
    method = kwargs.get("method", "GET")
    params = kwargs.get("params", "")
    query_params = kwargs.get("query_params", "")

    params = f"{params}"
    if query_params:
        params += f"{query_params}"
    if params:
        encoded = f"{params}".encode()
        params = f"_{hashlib.sha256(encoded).hexdigest()}"[:16]

    path = slugify(args[0])
    file_name = f"{method}{path}{params}.json"
    file_path = f"test/mock_data/{file_name}"
    if not Path(file_path).exists():
        with open(file_path, "w") as f:
            if r.text:
                print(f"Dumping response to '{file_name}'")
                json.dump(r.json(), f)
    return r


def setup_log():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    st = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(thread)d - %(filename)s:%(lineno)d - %(message)s")
    st.setFormatter(fmt)
    log.addHandler(st)
    return log


def main():
    dt = Dynatrace(os.getenv("DYNATRACE_TENANT_URL"), os.getenv("DYNATRACE_API_TOKEN"), log=setup_log())

    # TODO - Code here as you add new endpoints, during development
    # Any requests are going to be recorded in the `test/mock` folder and can later be used to write tests.
    for m in dt.metrics.list(page_size=500):
        print(m.metric_id)


if __name__ == "__main__":
    main()
