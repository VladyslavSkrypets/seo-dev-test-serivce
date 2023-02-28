from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from web.database.base import TableBase


class PageViewRegistrationModel(TableBase):
    __tablename__ = 'page_view_registration_table' # noqa

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    url_to_scan = Column(String, nullable=False)
    final_url = Column(String, nullable=False, default="")
    final_status_code = Column(Integer, nullable=True)
    status_code = Column(Integer, nullable=True)
    title = Column(String, nullable=False, default="")
    domain_name = Column(String, nullable=False, default="")
    datetime_utc = Column(DateTime, default=datetime.utcnow())
