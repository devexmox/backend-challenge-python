import pytest
from sqlalchemy import text

from moonbot.adapters.obstacle_repository import SQLAlchemyObstacleRepository


@pytest.fixture
def repository(session):
    return SQLAlchemyObstacleRepository(session)


@pytest.fixture
def obstacles():
    return {(1, 2), (2, 4), (2, 0)}


@pytest.fixture
def repository_with_obstacles(session, obstacles):
    repo = SQLAlchemyObstacleRepository(session)
    for obstacle in obstacles:
        repo.add(obstacle)
    repo._session.commit()
    return repo


def get_obstacles_from_db(session):
    obstacles = list(session.execute(text('SELECT * FROM "obstacle"')))
    return [(o[1], o[2]) for o in obstacles]  # strip id


def test_can_add_obstacle(repository):
    obstacle = (1, 2)
    repository.add(obstacle)
    repository._session.commit()
    obstacles = get_obstacles_from_db(repository._session)
    assert obstacles == [obstacle]


def test_adding_duplicate_obstacle_does_nothing(repository):
    obstacle = (1, 2)
    repository.add(obstacle)
    session = repository._session
    session.commit()
    obstacles = get_obstacles_from_db(session)
    repository.add(obstacle)
    session.commit()
    obstacles_after_duplicate_add = get_obstacles_from_db(session)
    assert obstacles == obstacles_after_duplicate_add


def test_can_get_obstacles(repository_with_obstacles, obstacles):
    obstacles_from_repo = repository_with_obstacles.get()
    assert obstacles_from_repo == obstacles
