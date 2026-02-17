import os
import re

import pytest
from requests import get, post
from starlette import status

e2e = pytest.mark.skipif("not config.getoption('e2e')")


@pytest.fixture
def api_url():
    return os.getenv("API_URL", "http://localhost:8080/")


def is_state_str(str_: str) -> bool:
    match = re.fullmatch(r"\(\-?\d, \-?\d\) (NORTH|EAST|SOUTH|WEST)", str_)
    return match is not None


@e2e
def test_get_current_position(api_url):
    response = get(api_url + "/state")
    assert response.status_code == status.HTTP_200_OK
    assert is_state_str(response.json())


@e2e
def test_move(api_url):
    response = post(api_url + "/move", params={"command": "FFFLF"})
    assert response.status_code == status.HTTP_200_OK
    assert is_state_str(response.json())
    response = get(api_url + "/state")
    assert response.status_code == status.HTTP_200_OK
    assert is_state_str(response.json())


@e2e
def test_move_invalid_command(api_url):
    response = post(api_url + "/move", params={"command": "invalid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
