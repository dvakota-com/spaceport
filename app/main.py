"""
SpacePort API - Space Travel Booking Platform
Version: 1.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import bookings, destinations, users, payments
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="SpacePort API",
    description="Book your journey to the stars",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - restrict to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://spaceport.io", "https://app.spaceport.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 routes
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(destinations.router, prefix="/api/v1/destinations", tags=["destinations"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
