from fastapi import FastAPI
from app.router.pools import router as pools
import time
from starlette.requests import Request


app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(pools)

@app.get("/")
async def root():
    return {"message": "Dex API is running"}