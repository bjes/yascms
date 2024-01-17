from invoke import task


@task(name='all')
def test_all(c):
    """Run all tests"""
    c.run('pytest')


@task(name='gen-cov')
def test_gen_cov(c):
    """Generate test coverage"""
    c.run('pytest --cov=yascms')

