from __future__ import annotations

import re
from itertools import chain
from typing import List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup
from pydantic import BaseModel

from web.utilities.logger import logging
from web.api.services.base import BaseInfoGather
from web.schemas.domain_statistic import PageData, Url


class DomainStatisticInfo(BaseModel, BaseInfoGather):
    active_page_count: int = 0
    total_page_count: int = 0
    url_list: List[str] = []

    @staticmethod
    def _parse_urls_with_domain_from_page_content(page_content: bytes, domain: str) -> List[str]:
        urls_pattern = re.compile(rf"^(http|https)://(www\.)?{re.escape(domain)}.*$")
        try:
            soup = BeautifulSoup(page_content, "html.parser")
            return list({
                Url(value=a_tag.get('href'))
                for a_tag in soup.find_all('a', attrs={'href': urls_pattern})
            })
        except Exception:
            logging.error("Error occurred during parsing urls with domain from page content", exc_info=True)
            return []

    def _search_page_links(self, url: str, domain: str) -> Optional[PageData]:
        response = self.get_url_response(url=url)
        if response is None:
            return None

        page_data = PageData(
            url=Url(value=url),
            is_active=response.ok,
            urls_list=self._parse_urls_with_domain_from_page_content(
                page_content=response.content,
                domain=domain
            )
        )
        return page_data

    def _request_many_pages(self, urls_to_scan: Set[Url]) -> List[PageData]:
        try:
            with ThreadPoolExecutor(max_workers=len(urls_to_scan)) as executor:
                futures = [
                    executor.submit(
                        self._search_page_links,
                        url.value,
                        self.parse_url_domain(url=url.value)
                    ) for url in urls_to_scan
                ]
                results = [future.result() for future in as_completed(futures) if as_completed(futures)]
                return [result for result in results if result is not None]
        except Exception:
            logging.error("Error occurred during requesting pages links", exc_info=True)
            return []

    def _calculate_data(self, visited_pages: Set[PageData]) -> DomainStatisticInfo:
        total_pages_urls = set(chain(*[page_data.urls_list for page_data in visited_pages]))
        active_pages_urls = {page_data for page_data in visited_pages if page_data.is_active}

        self.total_page_count = len(total_pages_urls)
        self.active_page_count = len(active_pages_urls)
        self.url_list = [page_url.value for page_url in total_pages_urls]
        return self

    def gather(self, domain_name: str, search_depth: int = 3) -> DomainStatisticInfo:
        visited_pages: Set[PageData] = set()

        urls_to_scan = {Url(value=f'https://{domain_name}')}
        for _ in range(search_depth + 1):  # one more iteration due to the first iteration is start url scan
            results = self._request_many_pages(urls_to_scan=urls_to_scan)

            new_scanned_pages_urls: Set[Url] = set(chain(*[page_data.urls_list for page_data in results]))
            visited_pages_urls = {page_data.url for page_data in visited_pages}

            urls_to_scan = new_scanned_pages_urls - visited_pages_urls

            visited_pages |= set(results)

        scanned_urls = {page_data.url for page_data in visited_pages}
        total_urls = set(chain(*[page_data.urls_list for page_data in visited_pages]))
        not_scanned_urls = total_urls - scanned_urls

        visited_pages |= set(self._request_many_pages(urls_to_scan=not_scanned_urls))

        return self._calculate_data(visited_pages=visited_pages)
