import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from web.config.manager import settings


TableBase = declarative_base()


class Database:
    def __init__(self) -> None:
        self.name = f'{settings.DATABASE_NAME}.db'
        self._db_file_path = os.path.dirname(__file__)

        self._engine = create_engine(
            f'sqlite:///{self._db_file_path}/{self.name}',
            pool_size=200,
            max_overflow=200,
            pool_timeout=300,
            pool_pre_ping=True,
            connect_args={"timeout": 60}
        )

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        if not os.path.exists(os.path.join(self._db_file_path, self.name)):
            TableBase.metadata.create_all(self._engine)

    def init(self) -> Session:
        db_ = self._session()
        return db_


@lru_cache()
def get_db() -> Session:
    return Database().init()

