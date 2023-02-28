from pydantic import BaseModel, AnyUrl


class PageViewRegistrationPayload(BaseModel):
    url: AnyUrl
