"""
SpacePort API - Space Travel Booking Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import bookings, destinations, users
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

# API v1 routes
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(destinations.router, prefix="/api/v1/destinations", tags=["destinations"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": settings.API_VERSION}
