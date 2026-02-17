import pytest

from moonbot.domain.bot import Bot, Direction


def pytest_addoption(parser):
    parser.addoption(
        "--e2e", action="store_true", dest="e2e", default=False, help="run e2e tests"
    )
