import pytest
from sqlalchemy import text

from moonbot.service.uow import SqlAlchemyUnitOfWork


@pytest.fixture
def uow(session):
    return SqlAlchemyUnitOfWork(lambda: session)


def test_rolls_back_on_exception(uow):
    class MyException(Exception):
        pass

    with pytest.raises(MyException):
        with uow:
            uow.commands.add("FF")
            raise MyException
    session = uow._session_factory()
    commands = list(session.execute(text("SELECT * FROM command")))
    assert commands == []


def test_does_not_commit_by_default(uow):
    with uow:
        uow.commands.add("FF")
    session = uow._session_factory()
    commands = list(session.execute(text("SELECT * FROM command")))
    assert commands == []


def test_commit(uow):
    command = "FF"
    with uow:
        uow.commands.add(command)
        uow.commit()
    session = uow._session_factory()
    commands = list(session.execute(text("SELECT * FROM command")))
    assert commands == [(1, command)]
