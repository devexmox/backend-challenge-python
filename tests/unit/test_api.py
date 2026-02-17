import pytest
from fastapi.testclient import TestClient

from moonbot.app.app import app, bot_service
from moonbot.domain.bot import Direction, State
from moonbot.service.bot_service import BotService
from tests.unit.utils import FakeUnitOfWork


@pytest.fixture
def uow():
    uow = FakeUnitOfWork()
    uow.bot_state.update(State(x=1, y=3, direction=Direction.EAST))
    uow.obstacles.add((3, 3))
    return uow


@pytest.fixture
def test_client(uow):
    override_bot_service = BotService(uow)
    app.dependency_overrides[bot_service] = lambda: override_bot_service
    return TestClient(app)


def test_moving_into_obstacle_appends_stopped_to_response(test_client):
    response = test_client.post("/move", params={"command": "FFF"})
    assert response.status_code == 200
    assert response.json() == "(2, 3) EAST STOPPED"
