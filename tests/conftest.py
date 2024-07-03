import pytest

pytest_plugins = [
    "tests.data_fixtures",
]


@pytest.fixture(scope="module", name="anyio_backend")
def fx_anyio_backend() -> str:
    """Specify the backend used for testing using anyio plugin.

    See more at:
    https://anyio.readthedocs.io/en/stable/testing.html#specifying-the-backends-to-run-on
    """
    return "asyncio"
