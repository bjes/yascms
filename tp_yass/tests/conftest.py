import pytest
from pyramid import testing

from tp_yass import routes


@pytest.fixture
def pyramid_config():
    config = testing.setUp()
    # 加入所有的 routes 定義，以便測試時不用再特別指定
    routes.includeme(config)
    yield config
    testing.tearDown()

