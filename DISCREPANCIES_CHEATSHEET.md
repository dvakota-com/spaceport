# SpacePort Demo - Discrepancies Cheat Sheet 🎯

This document lists ALL intentional discrepancies for demo verification.

---

## 📊 Code vs Documentation

### API Versioning
| Location | Documentation | Code |
|----------|---------------|------|
| README | v2.1.0 | v2.3.1 |
| Endpoints | /api/v1/* | /api/v2/* |

### Business Rules
| Rule | Documentation | Code | Jira |
|------|---------------|------|------|
| Early bird discount | 10% | 15% | - |
| Max passengers | 6 | 8 | - |
| Cancellation fee | 20% | 25% | SP-178 |
| Min age | 21 | 18 | - |
| Token expiration | 60 min | 30 min | - |
| Insurance fee | $299 | $500 | - |

### Field Naming
| Documentation | Code |
|---------------|------|
| display_name | full_name |
| num_travelers | passenger_count |
| final_amount | total_price |
| distance_miles | distance_km |

---

## 🚩 Jira Status vs Reality

| Jira ID | Status | Reality |
|---------|--------|---------|
| SP-142 | Done | CORS still allows * |
| SP-156 | Done | Feature flag = False |
| SP-189 | Done | No encryption |
| SP-190 | Done | Still MD5, not bcrypt |
| SP-201 | Done | Legacy endpoint exists |
| SP-203 | In Progress | Only TODO comment |
| SP-207 | Done | Only logs, no SendGrid |
| SP-208 | Backlog | SMS not implemented |
| SP-209 | Won't Fix | Push not implemented |
| SP-211 | Done | Bug still exists |

---

## 👻 Undocumented Features

- Crypto payments (5% discount)
- Diamond loyalty tier (20%)
- EMPLOYEE promo code (30%)
- VIPGUEST promo code (25%)
- 5% space travel tax
- Group discount 8% for 6+ pax
- risk_level field
- priority_score field
- REFUNDED booking status

---

## 🔐 Security Issues

1. **CORS** - allows all origins (*)
2. **MD5** - weak password hashing
3. **No auth** - on admin endpoints
4. **Passport** - stored unencrypted
5. **No rate limit** - on login
6. **PCI violation** - raw gateway response stored

---

## 📝 Git Commit -> Jira Mapping

| Commit Message | Jira | Discrepancy |
|----------------|------|-------------|
| "SP-142: Fix CORS" | Done | Still broken |
| "SP-156: Implement waitlist" | Done | Disabled |
| "SP-189: Encrypt passport" | Done | Not encrypted |
| "SP-190: Migrate to bcrypt" | Done | Still MD5 |
| "SP-211: Fix notifications" | Done | Still buggy |
