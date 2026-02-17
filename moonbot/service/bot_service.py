from moonbot.adapters.exceptions import BotStateNotFound
from moonbot.domain.bot import Bot, Direction, State, Status
from moonbot.service.uow import UnitOfWork

DEFAULT_BOT_STATE = State(x=0, y=0, direction=Direction.NORTH)


class BotService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def _maybe_initialize_bot_state(self):
        try:
            return self._uow.bot_state.get()
        except BotStateNotFound:
            self._uow.bot_state.update(DEFAULT_BOT_STATE)
            self._uow.commit()
            return DEFAULT_BOT_STATE

    def get_current_state(self) -> State:
        with self._uow:
            return self._maybe_initialize_bot_state()

    def move(self, command: str) -> tuple[State, Status]:
        with self._uow:
            state = self._maybe_initialize_bot_state()
            obstacles = self._uow.obstacles.get()
            bot = Bot(state.x, state.y, state.direction, obstacles=obstacles)
            status = bot.move(command)
            self._uow.bot_state.update(bot.state)
            self._uow.commands.add(command)
            self._uow.commit()
        return bot.state, status
