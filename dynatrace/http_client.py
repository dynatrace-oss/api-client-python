import logging
from typing import Dict, Optional
import time

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dynatrace.constants import TOO_MANY_REQUESTS_WAIT


class HttpClient:
    def __init__(
        self, base_url: str, token: str, log: logging.Logger = None, proxies: Dict = None, too_many_requests_strategy=None
    ):
        while base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

        if proxies is None:
            proxies = {}
        self.proxies = proxies

        self.auth_header = {"Authorization": f"Api-Token {token}"}
        self.log = log
        if self.log is None:
            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.WARNING)
            st = logging.StreamHandler()
            fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(thread)d - %(filename)s:%(lineno)d - %(message)s")
            st.setFormatter(fmt)
            self.log.addHandler(st)

        self.too_many_requests_strategy = too_many_requests_strategy

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

        self.log.debug(f"Making {method} request to '{url}' with params {params} and body: {body}")
        r = requests.request(method, url, headers=headers, params=params, json=body, verify=False, proxies=self.proxies)
        self.log.debug(f"Received response '{r}'")

        while r.status_code == 429 and self.too_many_requests_strategy == TOO_MANY_REQUESTS_WAIT:
            sleep_amount = int(r.headers.get("retry-after", 5))
            self.log.warning(f"Sleeping for {sleep_amount}s because we have received an HTTP 429")
            time.sleep(sleep_amount)
            r = requests.request(method, url, headers=headers, params=params, json=body, verify=False, proxies=self.proxies)

        if r.status_code >= 400:
            raise Exception(
                f"Error making request to {url}: {r}. Parameters: {params}, Body: {body}, Response: {r.text}, Headers: {r.headers}"
            )

        return r
