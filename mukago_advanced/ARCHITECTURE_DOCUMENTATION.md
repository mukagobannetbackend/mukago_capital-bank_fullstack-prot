# MUKAGO CAPITAL BANK - Full-Stack Architecture Documentation

**Project Version:** 1.0.0  
**Last Updated:** June 8, 2026  
**Status:** Production Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Database Design](#database-design)
6. [API Endpoints](#api-endpoints)
7. [Security Architecture](#security-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Development Guide](#development-guide)
10. [Performance Optimization](#performance-optimization)

---

## System Overview

MUKAGO CAPITAL BANK is a comprehensive fintech platform designed to deliver institutional-grade banking and investment services. The system is built using a modern microservices architecture with a React frontend, Flask backend, and PostgreSQL database.

### Key Characteristics

- **Multi-tenant Architecture:** Supports multiple users and organizations
- **Microservices Design:** Independent, scalable service components
- **Real-time Processing:** Instant transaction settlement and notifications
- **Enterprise Security:** Multi-layer security with encryption and compliance
- **Global Scale:** Multi-currency and multi-language support
- **High Availability:** Redundancy and failover mechanisms

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19, TypeScript, Tailwind CSS 4 | User interface and client-side logic |
| **Backend** | Flask, Python 3.11, Node.js | API server and business logic |
| **Database** | PostgreSQL 14, Redis | Data persistence and caching |
| **Infrastructure** | Docker, Kubernetes, AWS/GCP | Containerization and orchestration |
| **Security** | JWT, bcrypt, SSL/TLS | Authentication and encryption |

---

## Architecture Layers

### 1. Presentation Layer (Frontend)

The frontend is a single-page application (SPA) built with React 19, providing a responsive and interactive user interface.

**Responsibilities:**
- User interface rendering
- Client-side routing and navigation
- Form validation and data collection
- Real-time updates via WebSockets
- State management and caching

**Key Components:**
- Landing page with hero section
- User dashboard with account management
- Admin panel with system monitoring
- Trading interface for hedge fund operations
- Multi-language support (English, Spanish, French, Arabic, Chinese)

### 2. API Gateway Layer

The API Gateway acts as the entry point for all client requests, handling routing, authentication, and rate limiting.

**Responsibilities:**
- Request routing to appropriate microservices
- JWT token validation
- Rate limiting and throttling
- Request/response logging
- CORS handling

### 3. Business Logic Layer (Backend)

The backend implements core business logic through multiple microservices, each handling specific domains.

**Microservices:**
- **User Service:** Authentication and user management
- **Account Service:** Bank account operations
- **Transaction Service:** Payment and transfer processing
- **Investment Service:** Hedge fund and trading operations
- **Notification Service:** Real-time alerts and messaging
- **Admin Service:** System administration and monitoring

### 4. Data Access Layer

The data access layer manages all database operations through ORM (SQLAlchemy) and query optimization.

**Responsibilities:**
- Database connection management
- Query optimization and caching
- Transaction management
- Data validation and integrity

### 5. Database Layer

PostgreSQL serves as the primary data store with Redis for caching and session management.

**Components:**
- Primary database (Master)
- Read replicas for scaling
- Redis cache cluster
- Backup and recovery systems

---

## Backend Architecture

### Flask Application Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── models/
│   ├── user.py          # User model
│   ├── account.py       # Account model
│   ├── transaction.py   # Transaction model
│   └── investment.py    # Investment model
├── routes/
│   ├── auth.py          # Authentication endpoints
│   ├── accounts.py      # Account endpoints
│   ├── transactions.py  # Transaction endpoints
│   ├── investments.py   # Investment endpoints
│   └── admin.py         # Admin endpoints
├── services/
│   ├── user_service.py  # User business logic
│   ├── account_service.py
│   ├── transaction_service.py
│   └── investment_service.py
├── middleware/
│   ├── auth.py          # JWT authentication
│   ├── error_handler.py # Error handling
│   └── logging.py       # Request logging
└── utils/
    ├── validators.py    # Data validation
    ├── decorators.py    # Custom decorators
    └── helpers.py       # Utility functions
```

### Database Models

#### User Model
```python
class User:
    - id: Integer (Primary Key)
    - username: String (Unique)
    - email: String (Unique)
    - password_hash: String
    - full_name: String
    - role: String (user, admin, super_admin)
    - is_active: Boolean
    - created_at: DateTime
    - updated_at: DateTime
```

#### Account Model
```python
class Account:
    - id: Integer (Primary Key)
    - user_id: Integer (Foreign Key)
    - account_number: String (Unique)
    - account_type: String (savings, checking, investment)
    - balance: Float
    - currency: String
    - is_active: Boolean
    - created_at: DateTime
```

#### Transaction Model
```python
class Transaction:
    - id: Integer (Primary Key)
    - from_account_id: Integer (Foreign Key)
    - to_account_id: Integer (Foreign Key)
    - amount: Float
    - transaction_type: String (transfer, deposit, withdrawal)
    - status: String (completed, pending, failed)
    - description: String
    - created_at: DateTime
```

#### Investment Model
```python
class Investment:
    - id: Integer (Primary Key)
    - user_id: Integer (Foreign Key)
    - account_id: Integer (Foreign Key)
    - investment_type: String (stocks, bonds, crypto, hedge_fund)
    - symbol: String
    - quantity: Float
    - purchase_price: Float
    - current_price: Float
    - total_value: Float
    - created_at: DateTime
    - updated_at: DateTime
```

### API Response Format

All API responses follow a consistent JSON format:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "timestamp": "2026-06-08T10:30:00Z",
  "request_id": "req_12345"
}
```

### Error Handling

Errors are returned with appropriate HTTP status codes:

| Status Code | Meaning | Example |
|------------|---------|---------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Frontend Architecture

### React Application Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── robots.txt
├── src/
│   ├── index.tsx
│   ├── App.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Dashboard.tsx
│   │   ├── AdminDashboard.tsx
│   │   ├── Login.tsx
│   │   └── NotFound.tsx
│   ├── components/
│   │   ├── AdvancedCards.jsx
│   │   ├── AdminDashboard.jsx
│   │   ├── Navigation.tsx
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── styles/
│   │   ├── AdminDashboard.css
│   │   ├── AdvancedCards.css
│   │   ├── index.css
│   │   └── globals.css
│   ├── i18n/
│   │   ├── translations.js
│   │   └── useLanguage.js
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useApi.ts
│   │   └── useFetch.ts
│   ├── contexts/
│   │   ├── AuthContext.tsx
│   │   ├── ThemeContext.tsx
│   │   └── LanguageContext.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── storage.ts
│   └── utils/
│       ├── constants.ts
│       ├── validators.ts
│       └── formatters.ts
├── package.json
└── tsconfig.json
```

### State Management

The application uses React Context API for state management:

- **AuthContext:** User authentication state
- **ThemeContext:** Dark/light theme preference
- **LanguageContext:** Multi-language support

### Component Hierarchy

```
App
├── Header
│   ├── Logo
│   ├── Navigation
│   └── LanguageSwitcher
├── Main Content
│   ├── Home Page
│   │   ├── Hero Section
│   │   ├── Features Grid
│   │   ├── Modules Overview
│   │   └── Roadmap
│   ├── Dashboard
│   │   ├── Account Summary
│   │   ├── Transaction History
│   │   └── Portfolio Overview
│   └── Admin Dashboard
│       ├── Statistics
│       ├── User Management
│       └── System Monitoring
└── Footer
    ├── Links
    ├── Social Media
    └── Copyright
```

### API Integration

The frontend communicates with the backend through RESTful API calls using the Fetch API or Axios.

**Example API Call:**
```javascript
const fetchUserData = async (userId) => {
  try {
    const response = await fetch(`/api/users/${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) throw new Error('Failed to fetch user');
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};
```

### Multi-language Implementation

The application supports 5 languages with dynamic switching:

```javascript
// Usage in components
const { t, language, setLanguage } = useLanguage();

return (
  <div>
    <h1>{t('hero.title')}</h1>
    <select onChange={(e) => setLanguage(e.target.value)}>
      <option value="en">English</option>
      <option value="es">Español</option>
      <option value="fr">Français</option>
      <option value="ar">العربية</option>
      <option value="zh">中文</option>
    </select>
  </div>
);
```

---

## Database Design

### Schema Overview

The database uses a relational model with the following key relationships:

```
Users (1) ──→ (Many) Accounts
Users (1) ──→ (Many) Transactions
Users (1) ──→ (Many) Investments
Accounts (1) ──→ (Many) Transactions
Accounts (1) ──→ (Many) Investments
```

### Indexing Strategy

Key indexes for performance optimization:

| Table | Column | Type | Purpose |
|-------|--------|------|---------|
| users | email | Unique | Fast user lookup |
| users | username | Unique | Unique username constraint |
| accounts | user_id | Index | Fast account retrieval |
| accounts | account_number | Unique | Account identification |
| transactions | from_account_id | Index | Transaction history |
| transactions | to_account_id | Index | Transaction history |
| transactions | created_at | Index | Time-based queries |
| investments | user_id | Index | User portfolio lookup |
| investments | symbol | Index | Security lookup |

### Data Integrity

- **Foreign Key Constraints:** Ensure referential integrity
- **Unique Constraints:** Prevent duplicate entries
- **Check Constraints:** Validate data values
- **Triggers:** Automatic audit logging

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/logout` | User logout | Yes |
| POST | `/api/auth/refresh` | Refresh JWT token | Yes |

### User Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/users/{id}` | Get user details | Yes |
| GET | `/api/users` | List all users | Admin |
| PUT | `/api/users/{id}` | Update user | Yes |
| DELETE | `/api/users/{id}` | Delete user | Admin |

### Account Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/accounts` | Get user accounts | Yes |
| POST | `/api/accounts` | Create account | Yes |
| GET | `/api/accounts/{id}` | Get account details | Yes |
| PUT | `/api/accounts/{id}` | Update account | Yes |

### Transaction Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/transactions` | Get user transactions | Yes |
| POST | `/api/transactions` | Create transaction | Yes |
| GET | `/api/transactions/{id}` | Get transaction details | Yes |

### Investment Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/investments` | Get user investments | Yes |
| POST | `/api/investments` | Create investment | Yes |
| GET | `/api/investments/{id}` | Get investment details | Yes |
| PUT | `/api/investments/{id}` | Update investment | Yes |

### Admin Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/admin/dashboard` | Get dashboard stats | Admin |
| GET | `/api/admin/users` | List all users | Admin |
| PUT | `/api/admin/users/{id}/deactivate` | Deactivate user | Admin |
| GET | `/api/admin/logs` | Get activity logs | Admin |

---

## Security Architecture

### Authentication

**JWT (JSON Web Tokens):**
- Issued upon successful login
- Contains user ID and role information
- Expires after 24 hours
- Refresh tokens for extended sessions

**Password Security:**
- Bcrypt hashing with salt rounds = 10
- Minimum 8 characters required
- Must contain uppercase, lowercase, numbers, and symbols

### Authorization

**Role-Based Access Control (RBAC):**
- **User:** Basic account access
- **Admin:** System management and user administration
- **Super Admin:** Full system control

### Data Protection

**Encryption:**
- SSL/TLS for data in transit
- AES-256 for sensitive data at rest
- Encrypted database connections

**Data Validation:**
- Input sanitization to prevent SQL injection
- XSS protection through output encoding
- CSRF tokens for state-changing operations

### Compliance

- **GDPR:** User data privacy and right to be forgotten
- **PCI-DSS:** Payment card industry standards
- **SOC 2:** Security and compliance controls
- **Audit Logging:** All admin actions logged

---

## Deployment Architecture

### Containerization

**Docker:**
- Separate containers for frontend and backend
- Multi-stage builds for optimization
- Environment-specific configurations

**Kubernetes:**
- Orchestration and auto-scaling
- Service discovery and load balancing
- Rolling updates and zero-downtime deployments

### Infrastructure

**Cloud Platforms:**
- AWS (Recommended): EC2, RDS, S3, CloudFront
- Google Cloud: Compute Engine, Cloud SQL, Cloud Storage
- Azure: App Service, SQL Database, Blob Storage

**Load Balancing:**
- Application Load Balancer (ALB) for HTTP/HTTPS
- Network Load Balancer (NLB) for TCP/UDP
- Geographic distribution via CDN

### Monitoring and Logging

**Monitoring:**
- Prometheus for metrics collection
- Grafana for visualization
- CloudWatch for AWS monitoring

**Logging:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Centralized log aggregation
- Real-time alerting

---

## Development Guide

### Local Setup

**Backend Setup:**
```bash
# Clone repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
flask db upgrade

# Start development server
flask run
```

**Frontend Setup:**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start development server
npm start
# or
yarn start

# Build for production
npm run build
# or
yarn build
```

### Development Workflow

1. **Create Feature Branch:** `git checkout -b feature/feature-name`
2. **Make Changes:** Implement feature with tests
3. **Run Tests:** `npm test` and `pytest`
4. **Commit Changes:** `git commit -m "Add feature description"`
5. **Push to Remote:** `git push origin feature/feature-name`
6. **Create Pull Request:** Request code review
7. **Merge to Main:** After approval and CI/CD passes

### Testing

**Backend Testing:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

**Frontend Testing:**
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- --testNamePattern="Auth"
```

---

## Performance Optimization

### Backend Optimization

**Database Optimization:**
- Query optimization and indexing
- Connection pooling
- Caching frequently accessed data
- Pagination for large result sets

**API Optimization:**
- Response compression (gzip)
- Caching headers (ETag, Last-Modified)
- Rate limiting to prevent abuse
- Asynchronous processing for long operations

### Frontend Optimization

**Code Optimization:**
- Code splitting and lazy loading
- Tree shaking to remove unused code
- Minification and compression
- Image optimization and lazy loading

**Network Optimization:**
- HTTP/2 multiplexing
- Content Delivery Network (CDN)
- Service Worker for offline support
- Progressive Web App (PWA) capabilities

### Monitoring Performance

**Metrics:**
- Page load time
- Time to first contentful paint (FCP)
- Largest contentful paint (LCP)
- Cumulative layout shift (CLS)
- API response times

**Tools:**
- Google Lighthouse
- WebPageTest
- New Relic APM
- Datadog

---

## Conclusion

MUKAGO CAPITAL BANK represents a modern, scalable fintech platform built with industry best practices. The architecture supports high availability, security, and performance while maintaining flexibility for future enhancements and scaling.

For additional support and documentation, refer to the individual component READMEs and inline code comments.

**Document Version:** 1.0.0  
**Last Updated:** June 8, 2026  
**Author:** Manus AI
