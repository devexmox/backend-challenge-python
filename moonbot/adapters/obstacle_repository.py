from abc import ABC, abstractmethod

from sqlalchemy import func, select

from moonbot.adapters.orm import Obstacle


class ObstacleRepository(ABC):
    @abstractmethod
    def add(self, obstacle: tuple[int, int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> set[tuple[int, int]]:
        raise NotImplementedError


class SQLAlchemyObstacleRepository(ObstacleRepository):
    def __init__(self, session):
        self._session = session

    def _exists(self, obstacle: tuple[int, int]) -> bool:
        stmt = (
            select(func.count())
            .select_from(Obstacle)
            .where(Obstacle.x == obstacle[0], Obstacle.y == obstacle[1])
        )
        return self._session.scalar(stmt) > 0

    def add(self, obstacle: tuple[int, int]) -> None:
        if not self._exists(obstacle):
            self._session.add(Obstacle(x=obstacle[0], y=obstacle[1]))

    def get(self) -> set[tuple[int, int]]:
        query = self._session.scalars(select(Obstacle))
        return {(o.x, o.y) for o in query.all()}
