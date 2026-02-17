from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from moonbot.adapters.bot_repository import (
    BotStateRepository,
    SQLAlchemyBotStateRepository,
)
from moonbot.adapters.command_repository import (
    CommandRepository,
    SQLAlchemyCommandRepository,
)
from moonbot.adapters.obstacle_repository import (
    ObstacleRepository,
    SQLAlchemyObstacleRepository,
)
from moonbot.settings import settings


class UnitOfWork(ABC):
    bot_state: BotStateRepository
    commands: CommandRepository
    obstacles: ObstacleRepository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    create_engine(
        settings.DB_URI,
    )
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self._session_factory = session_factory

    def __enter__(self):
        self._session = self._session_factory()
        self.bot_state = SQLAlchemyBotStateRepository(self._session)
        self.commands = SQLAlchemyCommandRepository(self._session)
        self.obstacles = SQLAlchemyObstacleRepository(self._session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
