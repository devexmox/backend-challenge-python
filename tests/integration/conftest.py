import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from moonbot.adapters.orm import Base


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(engine)
    return session_factory()
