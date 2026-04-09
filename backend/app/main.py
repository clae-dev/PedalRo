from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import course, health

app = FastAPI(
    title="PedalRo API",
    description="AI 기반 자전거 관광 코스 큐레이션 서비스",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(course.router, prefix=settings.API_V1_PREFIX)
