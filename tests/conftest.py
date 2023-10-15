import pytest


@pytest.fixture(scope="session")
def entities_json_path(request):
    return request.config.rootdir / "/entities.json"


@pytest.fixture(scope="session")
def flags_json_path(request):
    return request.config.rootdir / "flags.json"
