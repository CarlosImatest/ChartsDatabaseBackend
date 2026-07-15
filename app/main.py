from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.user import router as user_router
from app.api.routes.chart import router as chart_router
from app.db.mongodb import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield
    # add any shutdown/cleanup logic here later (e.g. closing the Motor client)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(chart_router, prefix="/api/v1")