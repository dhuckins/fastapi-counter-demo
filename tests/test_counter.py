import pytest

from counter import counter


@pytest.mark.asyncio
async def test_counter(redis_dsn):
    cntr = counter.Counter(redis_dsn=redis_dsn)
    result = await cntr.get()
    assert result == 0

    new_value = 3
    result = await cntr.increment(amount=3)
    assert result == new_value

    result = await cntr.get()
    assert result == new_value

    result = await cntr.decrement(amount=2)
    assert result == 1
