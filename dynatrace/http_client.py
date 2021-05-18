import logging
from typing import Dict, Optional
import time

import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


TOO_MANY_REQUESTS_WAIT = "wait"


class DynatraceRetry(Retry):
    def get_backoff_time(self):
        return self.backoff_factor


class HttpClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        log: logging.Logger = None,
        proxies: Dict = None,
        too_many_requests_strategy=None,
        retries: int = 0,
        retry_delay_ms: int = 0,
        mc_jsession_id: Optional[str] = None,
        mc_b925d32c: Optional[str] = None,
        mc_sso_csrf_cookie: Optional[str] = None,
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
        retry_delay_s = retry_delay_ms / 1000

        try:
            self.retries = DynatraceRetry(
                total=retries,
                backoff_factor=retry_delay_s,
                status_forcelist=[400, 401, 403, 413, 429, 500, 502, 503, 504],
                allowed_methods=["TRACE", "PUT", "DELETE", "OPTIONS", "HEAD", "GET", "POST"],
                raise_on_status=False,
            )
        except TypeError:  # Older version of urllib3?
            self.retries = DynatraceRetry(
                total=retries,
                backoff_factor=retry_delay_s,
                status_forcelist=[400, 401, 403, 413, 429, 500, 502, 503, 504],
                method_whitelist=["TRACE", "PUT", "DELETE", "OPTIONS", "HEAD", "GET", "POST"],
                raise_on_status=False,
            )

        # This is for internal dynatrace usage
        self.mc_jsession_id = mc_jsession_id
        self.mc_b925d32c = mc_b925d32c
        self.mc_sso_csrf_cookie = mc_sso_csrf_cookie

    def make_request(self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, method="GET", data=None, files=None) -> requests.Response:
        url = f"{self.base_url}{path}"

        body = None
        if method in ["POST", "PUT"]:
            body = params
            params = None

        if headers is None:
            headers = {}
        if files is None and "content-type" not in [key.lower() for key in headers.keys()]:
            headers.update({"content-type": "application/json"})
        headers.update(self.auth_header)

        cookies = None
        if self.mc_b925d32c and self.mc_sso_csrf_cookie and self.mc_jsession_id:
            headers.update({"Cookie": f"JSESSIONID={self.mc_jsession_id}; ssoCSRFCookie={self.mc_sso_csrf_cookie}; b925d32c={self.mc_b925d32c}"})
            cookies = {"JSESSIONID": self.mc_jsession_id, "ssoCSRFCookie": self.mc_sso_csrf_cookie, "b925d32c": self.mc_b925d32c}

        s = requests.Session()
        s.mount("https://", HTTPAdapter(max_retries=self.retries))

        self.log.debug(f"Making {method} request to '{url}' with params {params} and body: {body}")
        r = s.request(method, url, headers=headers, params=params, json=body, verify=False, proxies=self.proxies, data=data, cookies=cookies, files=files)
        self.log.debug(f"Received response '{r}'")

        while r.status_code == 429 and self.too_many_requests_strategy == TOO_MANY_REQUESTS_WAIT:
            sleep_amount = int(r.headers.get("retry-after", 5))
            self.log.warning(f"Sleeping for {sleep_amount}s because we have received an HTTP 429")
            time.sleep(sleep_amount)
            r = requests.request(method, url, headers=headers, params=params, json=body, verify=False, proxies=self.proxies)

        if r.status_code >= 400:
            raise Exception(f"Error making request to {url}: {r}. Response: {r.text}")

        return r
