"""
SpacePort API - Space Travel Booking Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import bookings, destinations, users, payments
from app.core.config import settings

app = FastAPI(
    title="SpacePort API",
    description="Book your journey to the stars",
    version=settings.API_VERSION
)

# CORS Configuration - SP-142 (Fixed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v2 routes
app.include_router(bookings.router, prefix="/api/v2/bookings", tags=["bookings"])
app.include_router(destinations.router, prefix="/api/v2/destinations", tags=["destinations"])
app.include_router(users.router, prefix="/api/v2/users", tags=["users"])
app.include_router(payments.router, prefix="/api/v2/payments", tags=["payments"])

# Legacy v1 health endpoint - deprecated, will be removed per SP-201
@app.get("/api/v1/health")
async def legacy_health_check():
    """Deprecated: Use /api/v2/health instead"""
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/v2/health")
async def health_check():
    return {"status": "ok", "version": settings.API_VERSION}
