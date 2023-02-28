from typing import List
from pydantic import BaseModel, validator


class Url(BaseModel):
    value: str

    @validator('value')
    def clear_url(cls, url: str):  # noqa
        """
        For our inside calculations we need to clean the url due to the fact, that we deed exactly the page
        """
        url = url.split('#')[0]
        url = url.split('?')[0]

        if url.endswith('/'):
            url = url[0:-1]

        url.replace('www.', '')

        return url

    def __hash__(self) -> int:
        return hash(self.value)


class DomainStatisticPayload(BaseModel):
    domain_name: str


class PageData(BaseModel):
    url: Url
    is_active: bool
    urls_list: List[Url]

    def __hash__(self) -> int:
        return hash(self.url)
