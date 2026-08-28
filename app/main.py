from fastapi import FastAPI
from app.config import settings
from app.api.v1.ingestion import router as ingestion_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.dashboard import router as dashboard_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(ingestion_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}