from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from web.database.base import get_db
from web.utilities.logger import logging
from web.api.services.base import BaseInfoGather
from web.database.tables.page_view_registration import PageViewRegistrationModel


def save_page_view_registration_info(data: dict) -> None:
    db = get_db()
    model = PageViewRegistrationModel(**data)
    db.add(model)
    db.commit()


class PageViewRegistrationInfo(BaseModel, BaseInfoGather):
    final_url: str = ""
    final_status_code: Optional[int] = None
    status_code: Optional[int] = None
    title: str = ""
    domain_name: str = ""

    def parse_url_domain(self, url: str) -> PageViewRegistrationInfo:
        try:
            self.domain_name = super().parse_url_domain(url=url)
        except Exception:
            logging.error("Error occurred during parsing url domain", exc_info=True)
            pass

        return self

    def parse_site_title(self, response: requests.Response) -> PageViewRegistrationInfo:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            self.title = soup.title.string
        except Exception:
            logging.error("Error occurred during parsing site title", exc_info=True)

        return self

    def gather(self, url: str) -> PageViewRegistrationInfo:
        url_response = self.get_url_response(url=url)
        if url_response is None:
            return self

        self.parse_url_domain(url=url)
        self.parse_site_title(response=url_response)
        self.status_code = url_response.status_code

        if url_response.history:
            last_response = url_response.history[0]

            self.final_url = url_response.url
            self.status_code = last_response.status_code
            self.final_status_code = url_response.status_code

            self.parse_url_domain(url=url_response.url)

        return self
