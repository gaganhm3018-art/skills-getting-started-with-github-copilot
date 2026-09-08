from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    monkeypatch.setattr(app_module, "activities", deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client