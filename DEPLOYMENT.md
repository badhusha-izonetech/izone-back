# Backend Deployment Checklist

## Pre-Deployment Setup

### 1. Environment Variables
- [ ] Generate strong SECRET_KEY:
  ```bash
  python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
  ```
- [ ] Copy `.env.example` to `.env` in production
- [ ] Update all required environment variables:
  - `DATABASE_URL`: Production PostgreSQL connection
  - `SECRET_KEY`: Strong random 32+ character key
  - `ADMIN_USERNAME`: Strong unique username
  - `ADMIN_PASSWORD`: Strong unique password
  - `ALLOWED_ORIGINS`: Your frontend domain only (NO wildcards)
  - `DEBUG`: Set to `false`

### 2. Security Hardening
- [ ] Remove hardcoded credentials from code
- [ ] Verify `.gitignore` excludes `.env`, `venv/`, `__pycache__/`, `*.log`
- [ ] Ensure `.env` is NOT in git repository
- [ ] Review CORS configuration for your domain
- [ ] Enable HTTPS/TLS in production

### 3. Database Setup
- [ ] Create PostgreSQL database (e.g., `izoneweb_db`)
- [ ] Run migrations to create tables:
  ```bash
  cd backend
  .\venv\Scripts\python.exe init_tables.py
  ```
- [ ] Verify all tables created successfully
- [ ] Test database connection with health check endpoint

### 4. Dependencies
- [ ] Install all Python packages:
  ```bash
  .\venv\Scripts\pip.exe install -r requirements.txt
  ```
- [ ] Verify slowapi is installed for rate limiting
- [ ] Test imports: `.\venv\Scripts\python.exe -c "from app.config import *"`

### 5. Input Validation
- [ ] All public endpoints now validate:
  - Email format (EmailStr)
  - Phone numbers (7-20 chars with standard format)
  - Text field lengths (min/max constraints)
  - Numeric ranges (e.g., rating 1-5)
- [ ] Test API with invalid inputs to verify validation

### 6. Error Handling & Logging
- [ ] Logging configured for INFO level in production
- [ ] Verify error logs don't leak sensitive information
- [ ] Set up log rotation/archival for production logs
- [ ] Monitor logs for suspicious activity

### 7. Security Headers
- [ ] Verify API returns security headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Strict-Transport-Security: max-age=31536000`
  - `Content-Security-Policy: default-src 'self'`

### 8. Authentication
- [ ] Test login endpoint with correct/incorrect credentials
- [ ] Verify JWT tokens are properly signed
- [ ] Test token expiration
- [ ] Verify admin endpoints require valid token

### 9. Database Connection Validation
- [ ] Test health check endpoint: `GET /api/health`
- [ ] Verify database connection pooling is working
- [ ] Test graceful error handling if database goes down

### 10. API Testing
- [ ] Test all public endpoints (POST):
  - `/api/contacts` - Create contact
  - `/api/job-applications` - Submit job application
  - `/api/intern-applications` - Submit intern application
  - `/api/project-inquiries` - Submit project inquiry

- [ ] Test all admin endpoints (GET/PATCH/DELETE):
  - Verify authentication required
  - Verify proper authorization

### 11. Performance & Rate Limiting
- [ ] Rate limiting configured on public endpoints
- [ ] Monitor for bot/spam requests
- [ ] Database connection pool configured (min=1, max=10)

### 12. Documentation
- [ ] Generate OpenAPI docs (disabled in production)
- [ ] Document API endpoints for frontend team
- [ ] Document credential management
- [ ] Document monitoring/alerting setup

## Production Deployment Steps

```bash
# 1. Copy .env.example and configure for production
cp .env.example .env
# Edit .env with production values

# 2. Install dependencies
.\venv\Scripts\pip.exe install -r requirements.txt

# 3. Create database tables (if not already done)
.\venv\Scripts\python.exe init_tables.py

# 4. Run application on production server
# Using Gunicorn with 4 workers
.\venv\Scripts\gunicorn.exe -w 4 -b 0.0.0.0:8000 app.main:app

# Alternative: Using uvicorn with reload disabled
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Post-Deployment Verification

- [ ] Health check returns `{"status": "healthy", "database": "connected"}`
- [ ] API docs NOT accessible at `/docs` (DEBUG=false)
- [ ] CORS headers correct for production domain
- [ ] Logging captures all requests
- [ ] Database operations working correctly
- [ ] Authentication/authorization enforced
- [ ] Error messages don't leak sensitive info
- [ ] Security headers present in responses

## Monitoring & Maintenance

- [ ] Set up log aggregation (ELK, Splunk, etc.)
- [ ] Monitor database connection pool
- [ ] Track failed login attempts
- [ ] Set up alerts for errors
- [ ] Regular database backups
- [ ] Security patching schedule
- [ ] Rate limit monitoring

## Critical Issues Fixed in This Release

✅ Removed hardcoded credentials - now uses environment variables
✅ Added input validation - email, phone, length constraints
✅ Added error handling - try-catch with logging
✅ Added security headers - XSS, clickjacking, MIME-sniffing protection
✅ Fixed CORS - removed wildcard, uses allowed origins list
✅ Added logging - all operations logged for debugging
✅ Added health check - with database connectivity validation
✅ Improved authentication - proper error handling
