from typing import Generic, TypeVar, Iterator, TYPE_CHECKING

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

T = TypeVar("T", bound=DynatraceObject)


class PaginatedList(Generic[T]):
    def __init__(self, target_class, http_client, target_url, target_params=None, headers=None, list_item="result"):
        self.__elements = list()
        self.__target_class = target_class
        self.__http_client: HttpClient = http_client
        self.__target_url = target_url
        self.__target_params = target_params
        self.__headers = headers
        self.__list_item = list_item
        self._has_next_page = True
        self.__total_count = None
        self.__page_size = None

    def __getitem__(self, index):
        pass

    def __iter__(self) -> Iterator[T]:
        for element in self.__elements:
            yield element

        while self._has_next_page:
            new_elements = self._get_next_page()
            for element in new_elements:
                yield element

    def __len__(self):
        return self.__total_count or len(self.__elements)

    def _get_next_page(self):
        response = self.__http_client.make_request(self.__target_url, params=self.__target_params, headers=self.__headers)
        json_response = response.json()
        data = []
        if json_response.get("nextPageKey", None):
            self._has_next_page = True
            self.__target_params = {"nextPageKey": json_response["nextPageKey"]}
        else:
            self._has_next_page = False

        if self.__list_item in json_response:
            elements = json_response[self.__list_item]
            self.__total_count = json_response.get("totalCount") or len(elements)

            data = [self.__target_class(self.__http_client, response.headers, element) for element in elements]
        return data
