# Tender Intelligence AI

Enterprise-grade SaaS platform for Indian Government Tender & Procurement ecosystem.

## 🚀 Features

- **Advanced Search**: Semantic search with filters for location, category, value, deadlines
- **AI Analysis**: Automatic extraction of eligibility criteria, EMD, turnover requirements, risk scoring
- **Smart Alerts**: Real-time notifications via email, WhatsApp, SMS
- **Document Processing**: OCR and NLP-powered PDF analysis
- **Bid Analytics**: Historical data on awarded bidders, pricing trends
- **Team Collaboration**: Multi-user access with role-based permissions

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Next.js    │────▶│   FastAPI   │────▶│ PostgreSQL  │
│  Frontend   │     │    API      │     │   Database  │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Celery    │
                   │   Workers   │
                   └─────────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │  Redis   │ │Elastic   │ │   S3/R2  │
       │  Cache   │ │  Search  │ │  Storage │
       └──────────┘ └──────────┘ └──────────┘
```

## 🛠️ Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS + ShadCN UI
- Zustand (State Management)
- TanStack Query

### Backend
- FastAPI (Python)
- SQLAlchemy (Async)
- Celery (Task Queue)
- PostgreSQL
- Elasticsearch
- Redis

### Infrastructure
- Docker & Docker Compose
- Kubernetes ready
- CI/CD with GitHub Actions

## 📦 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose

### Development Setup

1. **Clone repository**
```bash
git clone <repository-url>
cd tender-intelligence-ai
```

2. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services with Docker**
```bash
npm run docker:up
```

4. **Or run locally**

Backend:
```bash
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Frontend:
```bash
cd apps/web
npm install
npm run dev
```

## 📊 API Documentation

Once running, access API docs at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🔒 Security

- JWT Authentication with refresh tokens
- RBAC (Role-Based Access Control)
- Rate limiting
- CORS protection
- SQL injection prevention
- XSS protection
- OWASP compliance

## 📈 Monitoring

- Prometheus metrics
- Grafana dashboards
- Sentry error tracking
- Structured logging

## 🧪 Testing

```bash
# Run tests
npm test

# Run E2E tests
npm run test:e2e

# Type checking
npm run typecheck
```

## 📄 License

Proprietary - All rights reserved

## 📞 Support

support@tenderintelligence.ai
