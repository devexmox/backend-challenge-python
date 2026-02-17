from enum import Enum

from pydantic import BaseModel, ConfigDict

from moonbot.domain.exceptions import InvalidCommand


class Direction(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Instruction(Enum):
    FORWARD = "F"
    BACK = "B"
    LEFT = "L"
    RIGHT = "R"


class State(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int
    y: int
    direction: Direction

    def __str__(self):
        return f"({self.x}, {self.y}) {self.direction.value}"

    @property
    def coords(self) -> tuple[int, int]:
        return (self.x, self.y)


class Status(Enum):
    SUCCESS = "success"
    STOPPED = "stopped"


class Bot:
    def __init__(
        self,
        x: int,
        y: int,
        direction: Direction,
        *,
        obstacles: set[tuple[int, int]] | None = None,
    ):
        self._state = State(x=x, y=y, direction=direction)
        self._obstacles = obstacles or set()

    @property
    def state(self) -> State:
        return self._state

    def _get_next_state_after_moving(
        self, instruction: Instruction, state: State
    ) -> tuple[State, bool]:
        direction_coeff = (
            1 if state.direction in [Direction.NORTH, Direction.EAST] else -1
        )
        move_coeff = 1 if instruction == Instruction.FORWARD else -1
        coord = "x" if state.direction in [Direction.WEST, Direction.EAST] else "y"
        update = {coord: getattr(state, coord) + direction_coeff * move_coeff}
        new_state = State(**update, **state.model_dump(exclude={coord}))
        if new_state.coords in self._obstacles:
            return (state, False)
        return (new_state, True)

    def _get_next_state_after_rotating(
        self, instruction: Instruction, state: State
    ) -> State:
        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        offset = 1 if instruction == Instruction.RIGHT else -1
        new_index = directions.index(state.direction) + offset
        new_direction = directions[new_index % len(directions)]
        return State(direction=new_direction, **state.model_dump(exclude={"direction"}))

    def move(self, command: str) -> Status:
        for letter in command:
            if letter not in Instruction:
                raise InvalidCommand(f'"{letter}" is not a valid command')
            instruction = Instruction(letter)
            match instruction:
                case Instruction.FORWARD | Instruction.BACK:
                    self._state, moved = self._get_next_state_after_moving(
                        instruction, self._state
                    )
                    if not moved:
                        return Status.STOPPED

                case Instruction.LEFT | Instruction.RIGHT:
                    self._state = self._get_next_state_after_rotating(
                        instruction, self._state
                    )
        return Status.SUCCESS
