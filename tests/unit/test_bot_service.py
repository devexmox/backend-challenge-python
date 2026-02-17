import re

import pytest

from moonbot.domain.bot import Bot, Direction, State, Status
from moonbot.service.bot_service import DEFAULT_BOT_STATE, BotService
from tests.unit.utils import FakeUnitOfWork


@pytest.fixture
def uow():
    uow = FakeUnitOfWork()
    uow.bot_state.update(State(x=1, y=2, direction=Direction.WEST))
    return uow


@pytest.fixture
def uow_no_bot_state():
    return FakeUnitOfWork()


def test_get_current_state(uow):
    bot_service = BotService(uow)
    state = bot_service.get_current_state()
    assert state
    assert state == uow.bot_state.get()


def test_move_returns_new_state_and_status(uow):
    bot_service = BotService(uow)
    old_state = bot_service.get_current_state()
    command = "FFRFLB"
    new_state, status = bot_service.move(command)
    bot = Bot(old_state.x, old_state.y, old_state.direction)
    bot.move(command)
    expected_state = bot.state
    assert new_state == expected_state
    assert status == Status.SUCCESS


def test_move_commits(uow):
    bot_service = BotService(uow)
    bot_service.move("FRFBLF")
    assert uow.commited


def test_move_saves_command(uow):
    bot_service = BotService(uow)
    command = "FRFBLF"
    bot_service.move(command)
    assert uow.commands._commands == [command]


def test_move_updates_bot_state(uow):
    bot_service = BotService(uow)
    command = "FFFFFF"
    bot_service.move(command)
    assert uow.commands._commands == [command]


def test_get_current_state_initializes_bot_state(uow_no_bot_state):
    bot_service = BotService(uow_no_bot_state)
    bot_service.get_current_state()
    state = uow_no_bot_state.bot_state.get()
    assert state == DEFAULT_BOT_STATE


def test_move_initializes_bot_state(uow_no_bot_state):
    bot_service = BotService(uow_no_bot_state)
    bot_service.move("BBFLRL")
    assert uow_no_bot_state.bot_state.get()


def test_move_into_obstacle(uow):
    uow.obstacles.add((-1, 2))
    bot_service = BotService(uow)
    state, status = bot_service.move("FFF")
    assert state == State(x=0, y=2, direction=Direction.WEST)
    assert status == Status.STOPPED
