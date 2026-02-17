import pytest

from moonbot.adapters.bot_repository import SQLAlchemyBotStateRepository
from moonbot.adapters.exceptions import BotStateNotFound
from moonbot.domain.bot import Direction, State


@pytest.fixture
def state():
    return State(x=1, y=2, direction=Direction.SOUTH)


@pytest.fixture
def empty_respository(session) -> SQLAlchemyBotStateRepository:
    return SQLAlchemyBotStateRepository(session)


@pytest.fixture
def repository(session, state) -> SQLAlchemyBotStateRepository:
    repo = SQLAlchemyBotStateRepository(session)
    repo.update(state)
    return repo


def test_updating_state_when_repository_empty_adds_it(empty_respository, state):
    empty_respository.update(state)
    empty_respository._session.commit()


def test_can_get_bot(repository, state):
    assert repository.get() == state


def test_trying_to_get_bot_when_repository_empty_raises_exception(empty_respository):
    with pytest.raises(BotStateNotFound):
        empty_respository.get()


def test_can_update_state(repository):
    state = repository.get()
    new_state = State(x=state.x + 1, y=state.y - 1, direction=state.direction)
    repository.update(new_state)
    saved_state = repository.get()
    assert saved_state == new_state
