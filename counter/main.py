import logging
import os
import pathlib

import fastapi
from fastapi import responses, staticfiles, templating

from . import api, counter

log = logging.getLogger(__name__)
HERE = pathlib.Path(__file__).absolute().parent


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI(debug=True)
    app.mount(
        path="/static",
        app=staticfiles.StaticFiles(directory=HERE / "static"),
        name="static",
    )
    templates = templating.Jinja2Templates(directory=HERE / "templates")

    @app.get("/", response_class=responses.HTMLResponse, include_in_schema=False)
    async def index(request: fastapi.Request):
        return templates.TemplateResponse(
            name="index.html", context={"request": request}
        )

    try:
        redis_dsn = os.environ["REDIS_URL"]
    except KeyError:
        log.error("please set `REDIS_URL`")
        raise

    cntr = counter.Counter(redis_dsn)
    app.middleware("http")(counter.middleware(cntr))

    app.include_router(router=api.router, prefix="/api/v1/counter")

    return app
