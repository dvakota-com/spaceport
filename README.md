# SpacePort API 🚀

> Book your journey to the stars

## Overview

SpacePort is a space travel booking platform that allows users to book trips to various celestial destinations including the Moon, Mars, and orbital stations.

## API Version

Current version: **2.1.0**

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

### Base URL
- Production: `https://api.spaceport.io/v1`
- Staging: `https://staging-api.spaceport.io/v1`

### Bookings

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/bookings` | Create new booking |
| GET | `/api/v1/bookings/{id}` | Get booking details |
| PUT | `/api/v1/bookings/{id}` | Update booking (pending only) |
| POST | `/api/v1/bookings/{id}/cancel` | Cancel booking |

### Business Rules

#### Booking Limits
- Maximum passengers per booking: **6**
- Minimum age requirement: **21 years**

#### Discounts
- Early bird (90+ days advance): **10%**
- Group booking (4+ passengers): **5%**
- Maximum combined discount: **25%**

#### Cancellation Policy
- More than 30 days before departure: Full refund minus **20%** fee
- 15-30 days: 50% refund
- Less than 15 days: No refund

### Authentication

Tokens expire after **60 minutes**.

Use RS256 algorithm for JWT validation.

### Payment Methods

Supported payment methods:
- Credit Card (Visa, Mastercard, Amex)
- Debit Card
- Bank Transfer

## Notification Channels

Users receive notifications via:
- ✅ Email
- ✅ SMS
- ✅ Push notifications

## Feature Status

| Feature | Status |
|---------|--------|
| Waitlist for sold-out destinations | ✅ Available |
| Crypto payments | ❌ Not available |
| Group discounts | ✅ Available |

## Changelog

### v2.1.0 (2024-08-01)
- Added waitlist feature (SP-156)
- Improved security with bcrypt password hashing (SP-190)
- Fixed CORS configuration (SP-142)

### v2.0.0 (2024-06-01)
- Migrated to API v2
- Added loyalty program
- Passport encryption (SP-189)

## Data Model

### User Fields
- `display_name` - User's display name
- `phone_number` - Required contact number

### Booking Fields
- `num_travelers` - Number of travelers
- `final_amount` - Final booking amount

### Destination Fields
- `distance_miles` - Distance in miles

## Contact

For API support, contact: api-support@spaceport.io
