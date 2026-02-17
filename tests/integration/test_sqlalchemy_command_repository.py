import pytest
from sqlalchemy import text

from moonbot.adapters.command_repository import SQLAlchemyCommandRepository


@pytest.fixture
def repository(session):
    return SQLAlchemyCommandRepository(session)


def test_can_add_command(repository):
    command = "FFBLFRRB"
    repository.add(command)

    session = repository._session
    session.commit()
    commands = list(session.execute(text('SELECT * FROM "command"')))
    assert commands == [(1, command)]
