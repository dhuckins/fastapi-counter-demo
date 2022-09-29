import fastapi
import pydantic

from .counter import Counter, get_counter

router = fastapi.APIRouter(tags=["count"])


class Body(pydantic.BaseModel):
    amount: int


@router.get("/")
async def get(
    counter: Counter = fastapi.Depends(get_counter),
) -> Body:
    result = await counter.get()
    return Body(amount=result)


@router.post("/")
async def incr(
    req: Body,
    counter: Counter = fastapi.Depends(get_counter),
) -> Body:
    result = await counter.increment(amount=req.amount)
    return Body(amount=result)


@router.delete("/")
async def decr(
    req: Body,
    counter: Counter = fastapi.Depends(get_counter),
) -> Body:
    result = await counter.decrement(req.amount)
    return Body(amount=result)
