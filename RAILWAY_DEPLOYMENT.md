# Deployment Guide

Instructions for deploying to Railway platform.

## Prerequisites

- Railway account (free tier works)
- Railway CLI tool

## CLI Installation

**Windows (PowerShell):**
```bash
iwr https://railway.app/install.ps1 | iex
```

**Using npm:**
```bash
npm install -g @railway/cli
```

## Deployment Steps

### 1. Authentication

```bash
railway login
```

### 2. Initialize Project

```bash
cd library-management
railway init
```

### 3. Add Database

```bash
railway add --database postgresql
```

### 4. Configure Environment

```bash
railway variables set DEBUG=False
railway variables set DJANGO_SETTINGS_MODULE=config.settings.production
railway variables set ALLOWED_HOSTS=.railway.app
railway variables set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
```

### 5. Deploy Application

```bash
railway up
```

### 6. Get Public URL

```bash
railway domain
```

## Environment Configuration

| Variable | Value |
|----------|-------|
| DATABASE_URL | Auto-configured |
| DEBUG | False |
| SECRET_KEY | Generate new |
| DJANGO_SETTINGS_MODULE | config.settings.production |
| ALLOWED_HOSTS | .railway.app |

## Management Commands

```bash
# View application logs
railway logs

# Open dashboard
railway open

# Execute Django commands
railway run python manage.py <command>

# Access database shell
railway connect postgresql
```

## Troubleshooting

**Build failures:**
- Check `railway logs` for errors
- Verify requirements.txt is complete

**Database issues:**
- Confirm DATABASE_URL is set
- Check PostgreSQL service status

**Static files:**
- Ensure collectstatic in build
- Check STATIC_ROOT setting

## Web Dashboard Deployment

Alternative to CLI:

1. Sign in at railway.app
2. Create new project
3. Add PostgreSQL service
4. Connect GitHub repository
5. Configure environment variables
6. Deploy

## Pricing

- Free tier: $5 monthly credit
- Hobby: $5/month
- No card required for trial
