from datetime import datetime

from dynatrace.http_client import HttpClient


class ClusterTimeService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def time(self) -> datetime:
        return datetime.utcfromtimestamp(float(self.__http_client.make_request("/api/v1/time").text) / 1000)
