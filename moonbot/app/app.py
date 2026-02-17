from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from starlette import status

from moonbot.domain.bot import Status
from moonbot.domain.exceptions import InvalidCommand
from moonbot.service.bot_service import BotService
from moonbot.service.uow import SqlAlchemyUnitOfWork

app = FastAPI()


def bot_service() -> BotService:
    return BotService(SqlAlchemyUnitOfWork())


@app.get("/state")
def get_state(bot_service: BotService = Depends(bot_service)):
    state = bot_service.get_current_state()
    return JSONResponse(str(state))


@app.post("/move")
def move(command: str, bot_service: BotService = Depends(bot_service)):
    try:
        state, bot_status = bot_service.move(command)
        ret = str(state)
        if bot_status == Status.STOPPED:
            ret += " STOPPED"
        return JSONResponse(str(ret))
    except InvalidCommand as e:
        return JSONResponse(str(e), status.HTTP_400_BAD_REQUEST)
