# MUKAGO CAPITAL BANK - Complete Setup & Installation Guide

**Version:** 1.0.0  
**Last Updated:** June 8, 2026

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Database Setup](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Running the Application](#running-the-application)
8. [Docker Deployment](#docker-deployment)
9. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Ubuntu 20.04+, macOS 11+, Windows 10+ |
| **CPU** | 2 cores minimum |
| **RAM** | 4 GB minimum |
| **Storage** | 10 GB free space |
| **Network** | Internet connection required |

### Recommended Requirements

| Component | Recommendation |
|-----------|-----------------|
| **OS** | Ubuntu 22.04 LTS |
| **CPU** | 4+ cores |
| **RAM** | 8 GB+ |
| **Storage** | 50 GB+ SSD |

---

## Prerequisites

### Required Software

Install the following software before proceeding:

#### 1. Node.js and npm

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**macOS:**
```bash
brew install node
```

**Windows:**
Download from https://nodejs.org/ and run the installer.

**Verify Installation:**
```bash
node --version  # Should be v18.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

#### 2. Python 3.11+

**Ubuntu/Debian:**
```bash
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
```

**macOS:**
```bash
brew install python@3.11
```

**Windows:**
Download from https://www.python.org/downloads/ and run the installer.

**Verify Installation:**
```bash
python3 --version  # Should be 3.11.0 or higher
```

#### 3. PostgreSQL 14+

**Ubuntu/Debian:**
```bash
sudo apt-get install -y postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/ and run the installer.

**Verify Installation:**
```bash
psql --version  # Should be 14.0 or higher
```

#### 4. Redis (Optional but Recommended)

**Ubuntu/Debian:**
```bash
sudo apt-get install -y redis-server
```

**macOS:**
```bash
brew install redis
```

**Windows:**
Download from https://github.com/microsoftarchive/redis/releases

#### 5. Git

**Ubuntu/Debian:**
```bash
sudo apt-get install -y git
```

**macOS:**
```bash
brew install git
```

**Windows:**
Download from https://git-scm.com/download/win

---

## Backend Setup

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd mukago_advanced/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Example .env Configuration:**
```
FLASK_ENV=development
FLASK_APP=app.py
DEBUG=True

DATABASE_URL=postgresql://user:password@localhost:5432/mukago_bank
JWT_SECRET_KEY=your-super-secret-key-change-in-production

SERVER_HOST=0.0.0.0
SERVER_PORT=5000

CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Step 5: Initialize Database

```bash
# Create database
createdb mukago_bank

# Run migrations (if using Alembic)
flask db upgrade

# Or create tables directly
python3 -c "from app import db, app; app.app_context().push(); db.create_all()"
```

### Step 6: Start Backend Server

```bash
flask run
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd ../frontend
```

### Step 2: Install Dependencies

```bash
npm install
# or
yarn install
```

### Step 3: Configure Environment Variables

```bash
# Create .env file
cat > .env << EOF
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=MUKAGO CAPITAL BANK
VITE_ENVIRONMENT=development
EOF
```

### Step 4: Start Development Server

```bash
npm start
# or
yarn start
```

**Expected Output:**
```
  VITE v4.x.x  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.x.x:3000/
```

---

## Database Setup

### PostgreSQL Configuration

#### 1. Create Database User

```bash
sudo -u postgres psql

# Inside psql:
CREATE USER mukago_user WITH PASSWORD 'secure_password';
ALTER ROLE mukago_user SET client_encoding TO 'utf8';
ALTER ROLE mukago_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE mukago_user SET default_transaction_deferrable TO on;
ALTER ROLE mukago_user SET timezone TO 'UTC';
```

#### 2. Create Database

```bash
# Inside psql:
CREATE DATABASE mukago_bank OWNER mukago_user;
GRANT ALL PRIVILEGES ON DATABASE mukago_bank TO mukago_user;
\q
```

#### 3. Verify Connection

```bash
psql -U mukago_user -d mukago_bank -h localhost
```

### Database Backup and Restore

**Create Backup:**
```bash
pg_dump -U mukago_user -d mukago_bank > backup.sql
```

**Restore from Backup:**
```bash
psql -U mukago_user -d mukago_bank < backup.sql
```

---

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development`, `production` |
| `FLASK_APP` | Flask application file | `app.py` |
| `DEBUG` | Debug mode | `True`, `False` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@localhost/db` |
| `JWT_SECRET_KEY` | JWT signing key | `your-secret-key` |
| `SERVER_HOST` | Server host address | `0.0.0.0` |
| `SERVER_PORT` | Server port | `5000` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:5000` |
| `VITE_APP_NAME` | Application name | `MUKAGO CAPITAL BANK` |
| `VITE_ENVIRONMENT` | Environment | `development`, `production` |

---

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
flask run
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Access Application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Admin Dashboard: http://localhost:3000/admin

### Production Mode

**Build Frontend:**
```bash
cd frontend
npm run build
```

**Start Production Server:**
```bash
cd backend
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Docker Deployment

### Prerequisites

Install Docker and Docker Compose:
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

### Build Docker Images

**Create Dockerfile for Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Create Dockerfile for Frontend:**
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose Configuration

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: mukago_user
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: mukago_bank
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://mukago_user:secure_password@postgres:5432/mukago_bank
      JWT_SECRET_KEY: your-secret-key
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (careful - deletes data)
docker-compose down -v
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port
lsof -i :5000  # For backend
lsof -i :3000  # For frontend

# Kill process
kill -9 <PID>

# Or use different port
PORT=5001 flask run
```

#### 2. Database Connection Error

**Error:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Verify connection
psql -U mukago_user -d mukago_bank -h localhost
```

#### 3. Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify virtual environment is activated
which python  # Should show venv path
```

#### 4. CORS Error

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
```bash
# Update CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Restart backend server
```

#### 5. Frontend Build Error

**Error:** `npm ERR! code ERESOLVE`

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install
```

### Debug Mode

**Enable Verbose Logging:**

Backend:
```bash
export FLASK_DEBUG=1
flask run
```

Frontend:
```bash
npm start -- --inspect
```

### Getting Help

1. Check logs for error messages
2. Review documentation files
3. Check GitHub issues
4. Contact support team

---

## Next Steps

After successful setup:

1. **Create Admin User:**
   ```bash
   python3 -c "from app import db, User, app; app.app_context().push(); admin = User(username='admin', email='admin@example.com', full_name='Admin User', role='super_admin'); admin.set_password('secure_password'); db.session.add(admin); db.session.commit(); print('Admin created')"
   ```

2. **Access Admin Dashboard:**
   - Navigate to http://localhost:3000/admin
   - Login with admin credentials

3. **Configure Settings:**
   - Set up email notifications
   - Configure payment gateways
   - Set up monitoring and alerts

4. **Run Tests:**
   ```bash
   # Backend
   pytest

   # Frontend
   npm test
   ```

5. **Deploy to Production:**
   - Follow deployment guide
   - Set up CI/CD pipeline
   - Configure monitoring

---

## Support and Documentation

- **Architecture Documentation:** See `ARCHITECTURE_DOCUMENTATION.md`
- **API Documentation:** See `API_DOCUMENTATION.md`
- **Development Guide:** See `DEVELOPMENT_GUIDE.md`

**Document Version:** 1.0.0  
**Last Updated:** June 8, 2026  
**Author:** Manus AI
