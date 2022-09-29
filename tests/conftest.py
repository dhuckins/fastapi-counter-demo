import pytest
from testcontainers import redis


@pytest.fixture(name="redis_dsn")
def _redis():
    """
    creates a redis container,
    provides the DSN,
    then closes the connection
    """
    port = 6379
    with redis.RedisContainer(port_to_expose=port) as container:
        dsn = (
            f"redis://{container.get_container_host_ip()}:"
            f"{container.get_exposed_port(port)}/0"
        )
        yield dsn
