# Tender Intelligence AI - Architecture Document

## Executive Summary

Tender Intelligence AI is an enterprise-grade SaaS platform for Indian Government Tender & Procurement ecosystem. It aggregates, indexes, analyzes, filters, monitors, and intelligently interprets tenders from thousands of government procurement sources.

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Web App   │  │  Mobile Web │  │   Admin     │  │   API       │    │
│  │  (Next.js)  │  │  (Next.js)  │  │  Dashboard  │  │  Clients    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CDN & EDGE LAYER                                 │
│                    Cloudflare CDN + WAF + DDoS                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        LOAD BALANCER LAYER                               │
│                      Nginx Reverse Proxy + SSL                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐                       │
│  │   Frontend Server   │  │   Backend API       │                       │
│  │   Next.js SSR/SSG   │  │   FastAPI (Async)   │                       │
│  │   Port: 3000        │  │   Port: 8000        │                       │
│  └─────────────────────┘  └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        MESSAGE QUEUE LAYER                               │
│                    Redis + Celery Workers                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │
│  │  Scraper    │  │   PDF AI    │  │ Notification│                      │
│  │  Workers    │  │   Workers   │  │  Workers    │                      │
│  └─────────────┘  └─────────────┘  └─────────────┘                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ PostgreSQL  │  │Elasticsearch│  │    Redis    │  │   AWS S3    │    │
│  │  (Primary)  │  │  (Search)   │  │  (Cache)    │  │  (Storage)  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript 5.x
- **Styling**: TailwindCSS 3.x + ShadCN UI
- **Animations**: Framer Motion
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts / Chart.js

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Async Runtime**: uvicorn + asyncio
- **API Style**: REST + WebSocket
- **Background Tasks**: Celery + Redis
- **Validation**: Pydantic v2

### Database
- **Primary DB**: PostgreSQL 15+
- **Search Engine**: Elasticsearch 8.x
- **Cache**: Redis 7.x
- **Object Storage**: AWS S3 / Cloudflare R2

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with ELK stack
- **APM**: Sentry

### Security
- **Authentication**: JWT + Refresh Tokens
- **OAuth**: Google Login
- **Rate Limiting**: Redis-based
- **WAF**: Cloudflare
- **Encryption**: AES-256 at rest, TLS 1.3 in transit

## Database Schema Design

### Core Tables

#### Users
```sql
- id: UUID (PK)
- email: VARCHAR(255) UNIQUE NOT NULL
- password_hash: VARCHAR(255)
- phone: VARCHAR(20)
- first_name: VARCHAR(100)
- last_name: VARCHAR(100)
- company_name: VARCHAR(255)
- gst_number: VARCHAR(20)
- pan_number: VARCHAR(10)
- role: ENUM('free', 'starter', 'professional', 'business', 'enterprise', 'admin')
- is_verified: BOOLEAN DEFAULT FALSE
- is_active: BOOLEAN DEFAULT TRUE
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- last_login: TIMESTAMP
```

#### Tenders
```sql
- id: UUID (PK)
- tender_id: VARCHAR(100) UNIQUE NOT NULL
- tender_number: VARCHAR(100)
- title: TEXT NOT NULL
- description: TEXT
- department: VARCHAR(255)
- buyer_name: VARCHAR(255)
- authority: VARCHAR(255)
- state: VARCHAR(100)
- district: VARCHAR(100)
- city: VARCHAR(100)
- pincode: VARCHAR(10)
- category: VARCHAR(100)
- sub_category: VARCHAR(100)
- procurement_type: ENUM('goods', 'services', 'works', 'consultancy')
- tender_type: ENUM('open', 'limited', 'single_source', 'ge_m')
- bid_value_min: DECIMAL(15,2)
- bid_value_max: DECIMAL(15,2)
- emd_amount: DECIMAL(15,2)
- currency: VARCHAR(3) DEFAULT 'INR'
- publish_date: DATE
- opening_date: DATE
- closing_date: DATE
- corrigendum_date: DATE
- status: ENUM('active', 'closed', 'cancelled', 'awarded', 'expired')
- source_url: TEXT
- source_portal: VARCHAR(100)
- pdf_urls: JSONB
- eligibility_criteria: JSONB
- technical_specifications: JSONB
- financial_criteria: JSONB
- documents_required: JSONB
- ai_summary: TEXT
- risk_score: INTEGER (0-100)
- complexity_score: INTEGER (0-100)
- qualification_probability: FLOAT (0-1)
- red_flags: JSONB
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- scraped_at: TIMESTAMP
```

#### Subscriptions
```sql
- id: UUID (PK)
- user_id: UUID (FK -> Users)
- plan_type: ENUM('free', 'starter', 'professional', 'business', 'enterprise')
- status: ENUM('active', 'cancelled', 'expired', 'past_due')
- start_date: DATE
- end_date: DATE
- amount: DECIMAL(10,2)
- currency: VARCHAR(3)
- payment_gateway: VARCHAR(50)
- payment_id: VARCHAR(100)
- order_id: VARCHAR(100)
- signature: TEXT
- auto_renew: BOOLEAN DEFAULT TRUE
- cancelled_at: TIMESTAMP
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### Alerts
```sql
- id: UUID (PK)
- user_id: UUID (FK -> Users)
- name: VARCHAR(255)
- keywords: JSONB
- filters: JSONB
- frequency: ENUM('instant', 'daily', 'weekly')
- channels: JSONB
- is_active: BOOLEAN DEFAULT TRUE
- last_sent_at: TIMESTAMP
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### SavedTenders
```sql
- id: UUID (PK)
- user_id: UUID (FK -> Users)
- tender_id: UUID (FK -> Tenders)
- notes: TEXT
- tags: JSONB
- created_at: TIMESTAMP
```

#### SearchHistory
```sql
- id: UUID (PK)
- user_id: UUID (FK -> Users)
- query: TEXT
- filters: JSONB
- results_count: INTEGER
- created_at: TIMESTAMP
```

#### AuditLogs
```sql
- id: UUID (PK)
- user_id: UUID (FK -> Users)
- action: VARCHAR(100)
- resource_type: VARCHAR(100)
- resource_id: UUID
- ip_address: INET
- user_agent: TEXT
- metadata: JSONB
- created_at: TIMESTAMP
```

## Indexing Strategy

### PostgreSQL Indexes
```sql
-- Tenders
CREATE INDEX idx_tenders_status ON tenders(status);
CREATE INDEX idx_tenders_closing_date ON tenders(closing_date);
CREATE INDEX idx_tenders_publish_date ON tenders(publish_date);
CREATE INDEX idx_tenders_state ON tenders(state);
CREATE INDEX idx_tenders_department ON tenders(department);
CREATE INDEX idx_tenders_category ON tenders(category);
CREATE INDEX idx_tenders_bid_value ON tenders(bid_value_min, bid_value_max);
CREATE INDEX idx_tenders_created_at ON tenders(created_at DESC);
CREATE INDEX idx_tenders_source_portal ON tenders(source_portal);
CREATE INDEX idx_tenders_full_text ON tenders USING gin(to_tsvector('english', title || ' ' || description));

-- Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Subscriptions
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_end_date ON subscriptions(end_date);

-- Alerts
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_active ON alerts(is_active);
```

### Elasticsearch Index Mapping
```json
{
  "mappings": {
    "properties": {
      "tender_id": {"type": "keyword"},
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {"type": "keyword"},
          "autocomplete": {"type": "text", "analyzer": "edge_ngram"}
        }
      },
      "description": {"type": "text", "analyzer": "standard"},
      "department": {"type": "keyword"},
      "state": {"type": "keyword"},
      "district": {"type": "keyword"},
      "category": {"type": "keyword"},
      "status": {"type": "keyword"},
      "closing_date": {"type": "date"},
      "publish_date": {"type": "date"},
      "bid_value_min": {"type": "float"},
      "bid_value_max": {"type": "float"},
      "location": {"type": "geo_point"},
      "ai_summary": {"type": "text"},
      "keywords": {"type": "keyword"}
    }
  }
}
```

## Scraping Architecture

### Distributed Scraping System

```
┌──────────────────────────────────────────────────────────────┐
│                    Scheduler (Celery Beat)                    │
│  - Daily full sync at 2 AM IST                               │
│  - Real-time sync every 30 minutes                           │
│  - Priority queue for urgent portals                         │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                  Queue Manager (Redis)                        │
│  - High priority: GeM, CPPP, Railways                        │
│  - Medium priority: State portals, PSUs                      │
│  - Low priority: Municipal, Universities                     │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                 Worker Pool (Celery Workers)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │  │ Worker N │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                  Scraper Engine                               │
│  - Playwright (primary)                                      │
│  - Puppeteer (fallback)                                      │
│  - Selenium (legacy support)                                 │
│  - Direct API (when available)                               │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                 Proxy Rotation Layer                          │
│  - Residential proxies                                       │
│  - Datacenter proxies                                        │
│  - Tor exit nodes (fallback)                                 │
│  - Automatic IP rotation                                     │
└──────────────────────────────────────────────────────────────┘
```

### Scraper Features
- Anti-bot bypass (headless browser fingerprinting)
- CAPTCHA solving integration (2Captcha API)
- Retry mechanism with exponential backoff
- Failure queue for manual review
- Duplicate detection using fuzzy matching
- Data normalization pipeline
- Corrigendum detection and linking
- Historical data tracking

## Notification Architecture

### Multi-Channel Notification System

```
User Preferences → Alert Engine → Channel Router → Delivery
                                            ├─ Email (SendGrid)
                                            ├─ SMS (Twilio/MSG91)
                                            ├─ WhatsApp (Meta API)
                                            ├─ Telegram (Bot API)
                                            └─ Push (Firebase)
```

### Alert Types
1. **Instant Alerts**: New matching tenders within 5 minutes
2. **Daily Digest**: Summary of all matching tenders
3. **Weekly Digest**: Analytics and trending opportunities
4. **Deadline Reminders**: 7 days, 3 days, 1 day before closing
5. **Corrigendum Alerts**: Updates to saved tenders

## Payment System Architecture

### Razorpay Integration Flow
```
User → Select Plan → Create Order → Razorpay Checkout 
→ Payment Success → Webhook → Verify Signature 
→ Activate Subscription → Send Invoice
```

### Stripe Integration Flow
```
User → Select Plan → Create Checkout Session → Stripe Hosted Page
→ Payment Success → Webhook → Create Customer 
→ Activate Subscription → Send Receipt
```

### Features
- GST-compliant invoicing
- Auto-renewal with retry logic
- Failed payment recovery (3 attempts)
- Prorated upgrades/downgrades
- Refund processing
- Coupon code system
- Free trial management

## RBAC Permissions Matrix

| Permission | Free | Starter | Professional | Business | Enterprise | Admin |
|------------|------|---------|--------------|----------|------------|-------|
| Daily Searches | 10 | 50 | 200 | 1000 | Unlimited | Unlimited |
| PDF Downloads | 0 | 5 | 25 | 100 | Unlimited | Unlimited |
| AI Analysis | 0 | 3 | 15 | 50 | Unlimited | Unlimited |
| Saved Tenders | 5 | 25 | 100 | 500 | Unlimited | Unlimited |
| Alerts | 1 | 3 | 10 | 25 | Unlimited | Unlimited |
| Team Members | 1 | 2 | 5 | 20 | 100 | N/A |
| API Access | No | No | Yes | Yes | Yes | Yes |
| Historical Data | 7 days | 30 days | 90 days | 1 year | 5 years | All |
| Export | No | CSV | CSV+Excel | All formats | All+API | All |
| Advanced Filters | Basic | Standard | Advanced | Premium | Enterprise | Full |

## SEO Architecture

### Programmatic SEO Pages
- `/tenders/{state}` - State-wise tenders
- `/tenders/{state}/{category}` - Category-wise
- `/tenders/{department}` - Department-wise
- `/tenders/closing-today` - Urgent tenders
- `/tenders/new-today` - Fresh tenders
- `/gem-tenders` - GeM specific
- `/railway-tenders` - Railway specific

### Technical SEO
- Server-side rendering (SSR)
- Dynamic sitemap.xml
- robots.txt optimization
- Schema.org markup (JobPosting, GovernmentService)
- Open Graph tags
- Twitter Cards
- Canonical URLs
- Breadcrumb navigation
- Internal linking strategy

## Multi-Tenant SaaS Architecture

### Tenant Isolation Strategy
- **Database**: Shared PostgreSQL with tenant_id column
- **Cache**: Redis with tenant prefix
- **Storage**: S3 with tenant folder structure
- **Queue**: Redis with tenant-specific queues

### Tenant Configuration
```python
class TenantConfig:
    tenant_id: str
    plan_type: str
    features: dict
    limits: dict
    branding: dict
    custom_domain: str
    api_keys: list
```

## Scaling Strategy

### Horizontal Scaling
- Stateless application servers
- Database read replicas
- Elasticsearch cluster
- Redis cluster
- Load balancer distribution

### Vertical Scaling
- Increase worker instances based on queue depth
- Auto-scaling based on CPU/memory usage
- Database connection pooling

### Caching Strategy
- Redis for session storage
- Redis for API response caching
- CDN for static assets
- Database query caching

### Performance Targets
- API response time: < 200ms (p95)
- Search response time: < 500ms (p95)
- Page load time: < 2s (FCP)
- Uptime: 99.9%

## Security Architecture

### Authentication Flow
```
Login → Validate Credentials → Generate JWT + Refresh Token
→ Store in HTTP-only cookies → Attach to requests
→ Validate on each request → Refresh when expired
```

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- API key authentication for integrations
- Rate limiting per user/plan

### Data Protection
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Secure file delivery with signed URLs
- PII data masking
- Audit logging

### Compliance
- GDPR readiness
- India DPDP Act 2023 compliance
- PCI-DSS for payments
- OWASP Top 10 mitigation

## Monitoring & Observability

### Metrics Collection
- Application metrics (Prometheus)
- Business metrics (custom)
- Infrastructure metrics (node exporter)

### Dashboards
- System health overview
- API performance
- Scraper status
- Revenue metrics
- User analytics

### Alerting
- Service downtime
- Error rate spikes
- Performance degradation
- Queue backlog
- Payment failures

## Disaster Recovery

### Backup Strategy
- PostgreSQL: Continuous WAL archiving + daily full backup
- Elasticsearch: Snapshot to S3 every 6 hours
- Redis: RDB snapshots every hour
- S3: Versioning enabled

### Recovery Objectives
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 1 hour

### Failover
- Multi-AZ deployment
- Database failover replicas
- Load balancer health checks
- Automatic container restart
