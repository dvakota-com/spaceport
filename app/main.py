"""
SpacePort API - Space Travel Booking Platform
Version: 2.3.1
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import bookings, destinations, users, payments
from app.core.config import settings
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="SpacePort API",
    description="Book your journey to the stars",
    version="2.3.1",  # Note: Confluence says 2.1.0
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production (JIRA: SP-142 - marked as Done but not fixed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v2 routes (Documentation still references v1)
app.include_router(bookings.router, prefix="/api/v2/bookings", tags=["bookings"])
app.include_router(destinations.router, prefix="/api/v2/destinations", tags=["destinations"])
app.include_router(users.router, prefix="/api/v2/users", tags=["users"])
app.include_router(payments.router, prefix="/api/v2/payments", tags=["payments"])

# Legacy v1 endpoint - should be removed per SP-201
@app.get("/api/v1/health")
async def legacy_health_check():
    """Deprecated: Use /api/v2/health instead"""
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/v2/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT
    }
