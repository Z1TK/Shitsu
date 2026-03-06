from fastapi import FastAPI, Request, HTTPException
import time

from backend.shitsu.controller.router import api_router
from backend.shitsu.app.logger import log

app = FastAPI()


@app.middleware("http")
async def log_requests(r: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(r)
    except HTTPException as e:
        log.warning(
            "HTTPException: %s %s - %d %s",
            r.method,
            r.url.path,
            e.status_code,
            e.detail,
        )
    duration = (time.time() - start_time) * 1000
    log.info(
        "%s %s - status: %d - duration: %.2fms",
        r.method,
        r.url.path,
        response.status_code,
        duration,
    )
    return response


app.include_router(api_router)
