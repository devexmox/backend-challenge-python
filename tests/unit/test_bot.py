import pytest
from pydantic import ValidationError

from moonbot.domain.bot import Bot, Direction, State, Status
from moonbot.domain.exceptions import InvalidCommand


@pytest.fixture
def bot() -> Bot:
    return Bot(1, 2, Direction.WEST)


def test_bot_returns_current_state(bot: Bot):
    assert bot.state == State(x=1, y=2, direction=Direction.WEST)


def test_bot_can_move_and_returns_status_success(bot: Bot):
    status = bot.move("FLFFFRFLB")
    assert bot.state == State(x=-1, y=0, direction=Direction.SOUTH)
    assert status == Status.SUCCESS


@pytest.mark.parametrize(
    "args",
    [
        (1, 2, "west"),
        (0.5, 3, Direction.WEST),
    ],
)
def test_validation_error_is_raised_on_invalid_constructor_arguments(args):
    with pytest.raises(ValidationError):
        Bot(*args)


def test_validation_error_is_raised_on_invalid_move_command(bot):
    with pytest.raises(InvalidCommand):
        bot.move("FLFINVALID")


def test_stops_before_an_obstacle_and_returns_status_stopped():
    bot = Bot(0, 0, Direction.NORTH, obstacles={(0, 2), (2, 3)})
    status = bot.move("FFFLR")
    assert bot.state == State(x=0, y=1, direction=Direction.NORTH)
    assert status == Status.STOPPED
