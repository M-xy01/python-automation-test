import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)


def _build_session():
    session = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class AdminApiClient:
    def __init__(self, base_url, timeout=10):
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.session = _build_session()
        self.token = None

    def login(self, username, password):
        url = f"{self.base}/auth/login"
        log.info("POST %s", url)
        resp = self.session.post(
            url,
            json={"username": username, "password": password},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        body = resp.json()
        if body.get("errno") == 0:
            self.token = body["data"]["token"]
            self.session.headers.update({"X-Litemall-Admin-Token": self.token})
        return body

    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def _request(self, method, path, **kwargs):
        url = self.base + path
        log.debug("%s %s", method, url)
        resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
        resp.raise_for_status()
        return resp.json()
