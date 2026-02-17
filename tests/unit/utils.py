from moonbot.adapters.bot_repository import BotStateRepository
from moonbot.adapters.command_repository import CommandRepository
from moonbot.adapters.exceptions import BotStateNotFound
from moonbot.adapters.obstacle_repository import ObstacleRepository
from moonbot.domain.bot import State
from moonbot.service.uow import UnitOfWork


class FakeBotStateRepository(BotStateRepository):
    def __init__(self):
        self._state = None

    def get(self) -> State:
        if self._state is None:
            raise BotStateNotFound
        return self._state

    def update(self, state: State) -> None:
        self._state = state


class FakeCommandRepository(CommandRepository):
    def __init__(self):
        self._commands = []

    def add(self, command: str) -> None:
        self._commands.append(command)


class FakeObstacleRepository(ObstacleRepository):
    def __init__(self):
        self._obstacles = set()

    def add(self, obstacle: tuple[int, int]) -> None:
        self._obstacles.add(obstacle)

    def get(self) -> set[tuple[int, int]]:
        return self._obstacles


class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.bot_state = FakeBotStateRepository()
        self.commands = FakeCommandRepository()
        self.obstacles = FakeObstacleRepository()
        self.commited = False

    def commit(self):
        self.commited = True

    def rollback(self):
        pass
