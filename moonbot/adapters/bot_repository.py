from abc import ABC, abstractmethod

from sqlalchemy import exc, select

from moonbot.adapters.exceptions import BotStateNotFound
from moonbot.adapters.orm import State as StateDAO
from moonbot.domain.bot import State


class BotStateRepository(ABC):
    @abstractmethod
    def get(self) -> State:
        raise NotImplementedError

    @abstractmethod
    def update(self, state: State) -> None:
        raise NotImplementedError


STATE_ID = "1"


class SQLAlchemyBotStateRepository(BotStateRepository):
    def __init__(self, session):
        self._session = session

    def _get_existing_dao(self) -> StateDAO | None:
        try:
            stmt = select(StateDAO).where(StateDAO.id == STATE_ID)
            return self._session.scalars(stmt).one()
        except exc.NoResultFound:
            return None

    def get(self) -> State:
        bot_dao = self._get_existing_dao()
        if bot_dao is None:
            raise BotStateNotFound
        return State(x=bot_dao.x, y=bot_dao.y, direction=bot_dao.direction)

    def update(self, state: State) -> None:
        state_dao = self._get_existing_dao()
        if state_dao is None:
            state_dao = StateDAO(id=STATE_ID)
        for k, v in state.model_dump().items():
            setattr(state_dao, k, v)
        self._session.add(state_dao)
