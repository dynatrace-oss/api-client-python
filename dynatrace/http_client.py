import logging
from typing import Dict, Optional

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

default_log = logging.getLogger("dynatrace_http_client")


class HttpClient:
    def __init__(self, base_url: str, token: str, log: logging.Logger = default_log, proxies: Dict = None):
        while base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

        if proxies is None:
            proxies = {}
        self.proxies = proxies

        self.auth_header = {"Authorization": f"Api-Token {token}"}
        self.log = log

    def make_request(
        self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, method="GET"
    ) -> requests.Response:
        url = f"{self.base_url}{path}"

        body = None
        if method in ["POST", "PUT"]:
            body = params
            params = None

        if headers is None:
            headers = {"content-type": "application/json"}
        headers.update(self.auth_header)

        self.log.debug(f"Making {method} request to '{url}' with params {params}")
        r = requests.request(method, url, headers=headers, params=params, json=body, verify=False, proxies=self.proxies)
        self.log.debug(f"Received response '{r}'")

        if r.status_code >= 400:
            raise Exception(f"Error making request to {url}: {r}. Response: {r.text}")
        return r
