# SpacePort API 🚀

> Book your journey to the stars

## Overview

SpacePort is a space travel booking platform.

## API Version

Current version: **2.1.0**

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

Base URL: `https://api.spaceport.io/v1`

### Bookings
- `POST /api/v1/bookings` - Create booking
- `GET /api/v1/bookings/{id}` - Get booking
- `POST /api/v1/bookings/{id}/cancel` - Cancel booking

### Business Rules

- Maximum passengers per booking: **6**
- Early bird discount (90+ days): **10%**
- Cancellation fee: **20%**

### Authentication

- Token expiration: **60 minutes**
- Algorithm: **RS256**

### Notifications

Users receive notifications via:
- ✅ Email
- ✅ SMS
- ✅ Push notifications

### Features

| Feature | Status |
|---------|--------|
| Waitlist | ✅ Available |
| Crypto payments | ❌ Not available |

## Changelog

### v2.1.0
- Added waitlist feature (SP-156)
- Security upgrade to bcrypt (SP-190)
- CORS fix (SP-142)
