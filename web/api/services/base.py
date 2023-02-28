from abc import ABC
from typing import Optional
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter, Retry
from fake_useragent import UserAgent


class BaseInfoGather(ABC):
    @staticmethod
    def get_url_response(url: str) -> Optional[requests.Response]:
        try:
            ua = UserAgent(use_external_data=True)

            session = requests.Session()

            retries = Retry(total=5, backoff_factor=0.2)

            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            response = session.get(
                url=url,
                allow_redirects=True,
                headers={'User-Agent': ua.random},
                timeout=60
            )
            return response

        except Exception:
            pass

    def parse_url_domain(self, url: str) -> str:
        return urlparse(url).netloc
