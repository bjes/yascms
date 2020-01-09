import pytest
from pyramid import testing


@pytest.fixture
def pyramid_config():
    config = testing.setUp()
    yield config
    testing.tearDown()
