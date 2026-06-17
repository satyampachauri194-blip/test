# Tender Intelligence AI

Enterprise-grade SaaS platform for Indian Government Tender & Procurement ecosystem.

## Overview

Tender Intelligence AI aggregates, indexes, analyzes, filters, monitors, and intelligently interprets tenders from thousands of government procurement sources including GeM, CPPP, state eProcurement portals, PSU procurement portals, railways, municipal corporations, and more.

## Features

- **Advanced Search**: Full-text search with Elasticsearch, fuzzy matching, semantic search
- **AI Analysis**: Automatic PDF extraction, risk scoring, qualification probability
- **Smart Alerts**: Real-time notifications via Email, SMS, WhatsApp, Telegram
- **Subscription Plans**: Free, Starter, Professional, Business, Enterprise tiers
- **Secure Authentication**: JWT tokens, OAuth (Google), role-based access control
- **Payment Integration**: Razorpay and Stripe support with GST invoicing

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL with asyncpg
- Redis for caching and message queue
- Elasticsearch for search
- Celery for background tasks
- Playwright for web scraping

### Frontend
- Next.js 14+ with App Router
- TypeScript
- TailwindCSS + ShadCN UI
- Zustand for state management
- TanStack Query for data fetching

### Infrastructure
- Docker & Docker Compose
- Kubernetes ready
- CI/CD with GitHub Actions
- Prometheus + Grafana monitoring

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Using Docker Compose

```bash
# Clone repository
cd tender-intelligence-ai

# Copy environment file
cp backend/.env.example backend/.env

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Access services
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
tender-intelligence-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API route handlers
│   │   ├── core/                # Configuration, security
│   │   ├── db/                  # Database session
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── security/            # Auth, permissions
│   │   ├── services/            # Business logic
│   │   ├── workers/             # Celery tasks
│   │   └── utils/               # Utilities
│   ├── tests/                   # Test files
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                     # Next.js app router
│   ├── components/              # React components
│   ├── hooks/                   # Custom hooks
│   ├── lib/                     # Utilities
│   └── public/                  # Static assets
├── infrastructure/
│   ├── docker/                  # Docker configs
│   ├── k8s/                     # Kubernetes manifests
│   └── nginx/                   # Nginx configs
├── docker-compose.yml
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/tenders` | GET | List tenders |
| `/api/v1/tenders/{id}` | GET | Get tender details |
| `/api/v1/search` | GET | Advanced search |
| `/api/v1/alerts` | GET/POST | Manage alerts |
| `/api/v1/subscriptions/plans` | GET | Get subscription plans |
| `/api/v1/payments` | POST | Create payment |

## Subscription Plans

| Plan | Monthly | Yearly | Features |
|------|---------|--------|----------|
| Free | ₹0 | ₹0 | 10 searches/day, 5 saved tenders |
| Starter | ₹999 | ₹9,999 | 50 searches, 5 PDFs, 3 AI analyses |
| Professional | ₹2,499 | ₹24,999 | 200 searches, 25 PDFs, API access |
| Business | ₹4,999 | ₹49,999 | 1000 searches, 100 PDFs, team collaboration |
| Enterprise | ₹9,999 | ₹99,999 | Unlimited, dedicated support |

## Environment Variables

See `backend/.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `REDIS_URL`: Redis connection string
- `ELASTICSEARCH_URL`: Elasticsearch URL
- `RAZORPAY_KEY_ID`: Razorpay API key
- `OPENAI_API_KEY`: OpenAI API key for AI features

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Deployment

### Production Deployment

1. Build production images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f infrastructure/k8s/
```

3. Configure Cloudflare for CDN and WAF

### Monitoring

- Prometheus metrics at `/metrics`
- Grafana dashboards for system health
- Sentry for error tracking

## Security

- JWT authentication with refresh tokens
- Rate limiting per user/plan
- SQL injection prevention (parameterized queries)
- XSS protection (security headers)
- CSRF protection
- OWASP Top 10 compliance

## License

Proprietary - All rights reserved

## Support

Email: support@tenderintelligence.ai
