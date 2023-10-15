import pytest


@pytest.fixture(scope="session")
def entities_json_path():
    return "/Users/yassinkortam/Documents/GitHub/ALEX-classify/entities.json"


@pytest.fixture(scope="session")
def flags_json_path():
    return "/Users/yassinkortam/Documents/GitHub/ALEX-classify/flags.json"


@pytest.fixture(scope="session")
def docs_dir():
    return "docs"
