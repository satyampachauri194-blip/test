# Tender Intelligence AI - Enterprise SaaS Platform

## Executive Summary

A production-ready, enterprise-grade SaaS platform for Indian Government Tender & Procurement ecosystem. This platform aggregates, indexes, analyzes, filters, monitors, and intelligently interprets tenders from thousands of government sources using advanced AI/ML capabilities.

## Architecture Overview

### System Design Principles

1. **Microservices Architecture**: Separated concerns for web, API, and background workers
2. **Event-Driven Design**: Async processing with message queues
3. **Multi-tenant SaaS**: Isolated data with shared infrastructure
4. **Horizontal Scalability**: Statelessservices for easy scaling
5. **Fault Tolerance**: Retry mechanisms, circuit breakers, and fallback strategies

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloudflare CDN                         │
│                   (DDoS Protection, Cache)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Nginx Reverse Proxy                    │
│                   (SSL Termination, Routing)                │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
    ┌─────────────────┐ ┌───────────┐ ┌──────────────┐
    │   Next.js Web   │ │ FastAPI   │ │   Admin      │
    │   (Frontend)    │ │   API     │ │   Panel      │
    └─────────────────┘ └───────────┘ └──────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                  Redis Cluster                          │
    │         (Cache, Session, Rate Limiting, Queue)          │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │               PostgreSQL (Primary DB)                   │
    │            (Tenders, Users, Subscriptions)              │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │              Elasticsearch (Search Engine)              │
    │           (Full-text, Semantic, Aggregations)           │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │              Celery Workers (Background Jobs)           │
    │     (Scraping, AI Processing, Notifications, PDFs)      │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                  AWS S3 / Cloudflare R2                 │
    │              (PDF Storage, Static Assets)               │
    └─────────────────────────────────────────────────────────┘
```

## Tech Stack Justification

### Frontend (Next.js + TypeScript)
- **SSR/SSG**: Critical for SEO performance on tender listing pages
- **App Router**: Modern React patterns, server components for performance
- **TypeScript**: Type safety across large codebase
- **TailwindCSS + ShadCN**: Rapid UI development with consistent design system
- **Zustand**: Lightweight state management vs Redux overhead
- **TanStack Query**: Efficient server state management with caching

### Backend (FastAPI + Python)
- **Async/Await**: High concurrency for I/O operations (scraping, DB queries)
- **Pydantic**: Automatic validation and serialization
- **Auto-generated OpenAPI**: Documentation and client generation
- **Python Ecosystem**: Rich libraries for scraping, AI/ML, data processing

### Database (PostgreSQL)
- **JSONB Support**: Flexible schema for varying tender structures
- **Full-text Search**: Complementary to Elasticsearch
- **Row-level Security**: Multi-tenant isolation
- **Partitioning**: Handle millions of tender records
- **ACID Compliance**: Critical for payment transactions

### Search (Elasticsearch)
- **Sub-second Search**: Required for user experience
- **Fuzzy Matching**: Handle typos in tender searches
- **Aggregations**: Analytics and filtering
- **Semantic Search**: AI-powered relevance ranking

### Queue (Celery + Redis)
- **Distributed Tasks**: Parallel scraping across multiple sources
- **Retry Logic**: Automatic retry on failures
- **Scheduling**: Cron-like jobs for periodic scraping
- **Priority Queues**: Urgent notifications vs batch processing

### Infrastructure
- **Docker**: Consistent environments across dev/staging/prod
- **Kubernetes**: Auto-scaling, self-healing, rolling deployments
- **Prometheus + Grafana**: Real-time monitoring and alerting
- **Sentry**: Error tracking and performance monitoring

## Database Schema Design

### Core Entities

1. **Users**: Authentication, profile, preferences
2. **Organizations**: Multi-tenant structure, team management
3. **Subscriptions**: Plans, billing, feature access
4. **Tenders**: Core tender data with normalized structure
5. **TenderDocuments**: PDFs, corrigendums, attachments
6. **Searches**: Saved searches, alerts
7. **Notifications**: Delivery tracking, preferences
8. **ScrapeJobs**: Monitoring scraper health
9. **AIAnalyses**: Cached AI results for tenders
10. **AuditLogs**: Compliance and security tracking

### Indexing Strategy

1. **Tenders**:
   - Composite index on (status, publish_date, closing_date)
   - GIN index on JSONB fields for flexible filtering
   - Full-text search index on title, description, keywords
   - Geospatial index for location-based queries

2. **Users**:
   - Unique index on email
   - Index on organization_id for team queries

3. **Searches**:
   - Index on user_id and is_active for alert processing

4. **Elasticsearch**:
   - Custom analyzers for Indian government terminology
   - Synonym filters for common abbreviations (PSU, PWD, etc.)
   - Completion suggester for autocomplete

## Scraping Architecture

### Distributed Scraper Design

```
┌─────────────────────────────────────────────────────────┐
│              Scraper Coordinator                        │
│         (Job Distribution, Health Monitoring)           │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ Scraper  │   │ Scraper  │   │ Scraper  │
  │ Worker 1 │   │ Worker 2 │   │ Worker N │
  └──────────┘   └──────────┘   └──────────┘
        │               │               │
        ▼               ▼               ▼
  ┌──────────────────────────────────────────┐
  │        Proxy Rotation Pool               │
  │    (Residential + Datacenter Proxies)    │
  └──────────────────────────────────────────┘
```

### Anti-Detection Strategies

1. **Browser Fingerprint Randomization**
2. **Request Timing Jitter**
3. **User-Agent Rotation**
4. **Header Consistency Validation**
5. **Cookie Management**
6. **JavaScript Challenge Solving**
7. **CAPTCHA Handling (2Captcha integration)**

### Data Normalization Pipeline

1. **Raw HTML/PDF** → **Structured Extraction**
2. **Schema Mapping** → **Canonical Tender Model**
3. **Duplicate Detection** (fuzzy matching on title + date + value)
4. **Enrichment** (department classification, location geocoding)
5. **Validation** (required fields, date consistency)
6. **Indexing** (PostgreSQL + Elasticsearch)

## AI/ML Pipeline

### PDF Processing Flow

1. **Download** → S3 temporary storage
2. **OCR** (if scanned) → Tesseract + layout analysis
3. **Text Extraction** → PyPDF2/pdfplumber
4. **Section Classification** → Fine-tuned BERT model
5. **Entity Extraction** → Custom NER for:
   - EMD amounts
   - Turnover requirements
   - Experience criteria
   - Technical specifications
   - Eligibility clauses
6. **Risk Analysis** → Rule-based + ML scoring
7. **Summary Generation** → LLM (Llama 2/Mistral self-hosted)

### Risk Scoring Model

Features:
- Contradictory clauses count
- Unusual payment terms
- High liquidated damages
- Vague technical specs
- Short bid preparation time
- High EMD relative to bid value
- Past buyer complaint history

Output: 0-100 risk score with explainability

## Subscription & Monetization

### Plan Structure

| Feature | Free | Starter | Professional | Business | Enterprise |
|---------|------|---------|--------------|----------|------------|
| Daily Searches | 10 | 100 | 500 | 2000 | Unlimited |
| PDF Downloads | 0 | 20 | 100 | 500 | Unlimited |
| AI Analyses | 0 | 5 | 50 | 200 | Unlimited |
| Email Alerts | 1 | 5 | 20 | 50 | Unlimited |
| Team Members | 1 | 3 | 10 | 50 | Unlimited |
| API Access | ❌ | ❌ | ✅ | ✅ | ✅ |
| Historical Data | 7 days | 30 days | 1 year | 5 years | Unlimited |
| Priority Support | ❌ | ❌ | ❌ | ✅ | ✅ |

### Payment Flow

1. **Plan Selection** → Razorpay/Stripe Checkout
2. **Payment Verification** → Webhook validation
3. **Subscription Activation** → Update user entitlements
4. **Invoice Generation** → GST-compliant PDF
5. **Recurring Billing** → Auto-renewal handling
6. **Dunning Management** → Failed payment recovery

## Security Architecture

### Authentication Flow

1. **JWT Access Token** (15 min expiry)
2. **Refresh Token** (7 days, stored in HttpOnly cookie)
3. **Token Rotation** on each refresh
4. **Revocation List** for logout/banned users

### RBAC Matrix

| Role | View Tenders | Save Tenders | AI Analysis | Team Mgmt | Billing | Admin |
|------|-------------|--------------|-------------|-----------|---------|-------|
| Free User | ✅ | 10 | ❌ | ❌ | ❌ | ❌ |
| Subscriber | ✅ | Unlimited | ✅ | ❌ | Own | ❌ |
| Team Admin | ✅ | Unlimited | ✅ | ✅ | ✅ | ❌ |
| Org Owner | ✅ | Unlimited | ✅ | ✅ | ✅ | ❌ |
| Support | ✅ | ✅ | ✅ | ❌ | ❌ | Partial |
| Super Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### OWASP Top 10 Mitigations

1. **Injection**: Parameterized queries, ORM usage
2. **Broken Auth**: MFA support, session management
3. **Sensitive Data**: Encryption at rest (AES-256) and transit (TLS 1.3)
4. **XXE**: XML parser hardening
5. **Broken Access Control**: Middleware authorization checks
6. **Security Misconfiguration**: Automated security scanning
7. **XSS**: CSP headers, output encoding
8. **Insecure Deserialization**: Safe serialization formats
9. **Vulnerable Components**: SCA with Dependabot
10. **Insufficient Logging**: Structured logs with SIEM integration

## SEO Strategy

### Programmatic SEO Pages

Generate static pages for high-intent keywords:
- `/tenders/{state}/{category}`
- `/tenders/{department}/{location}`
- `/gem-tenders/{category}`
- `/active-tenders/{industry}`

### Technical SEO

1. **Server-Side Rendering**: Critical content rendered on server
2. **Structured Data**: Schema.org markup for tenders
3. **XML Sitemap**: Dynamic sitemap with priority scoring
4. **Robots.txt**: Crawl budget optimization
5. **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
6. **Canonical URLs**: Prevent duplicate content
7. **Internal Linking**: Related tenders, category hierarchies

## Scaling Strategy

### Horizontal Scaling

1. **Stateless Services**: Any instance can handle any request
2. **Database Read Replicas**: Separate read/write workloads
3. **Sharding**: By organization_id for multi-tenant isolation
4. **CDN Caching**: Static assets, API responses (where appropriate)

### Vertical Scaling

1. **Memory Optimization**: Connection pooling, query optimization
2. **CPU-bound Tasks**: Offload to workers (AI processing, OCR)
3. **I/O-bound Tasks**: Async I/O, connection reuse

### Caching Strategy

1. **L1 Cache**: In-memory (node-cache) for frequently accessed data
2. **L2 Cache**: Redis for shared cache across instances
3. **CDN Cache**: Edge caching for static content
4. **Query Cache**: Database query result caching
5. **Invalidation**: TTL-based + event-driven invalidation

## Monitoring & Observability

### Metrics Collection

1. **Business Metrics**:
   - Active users, conversions, churn
   - Tenders scraped per source
   - Search success rate
   - Alert delivery rate

2. **Technical Metrics**:
   - Request latency (p50, p95, p99)
   - Error rates by endpoint
   - Database query performance
   - Cache hit rates
   - Queue depths

3. **Infrastructure Metrics**:
   - CPU/Memory utilization
   - Disk I/O
   - Network throughput
   - Container health

### Alerting Rules

1. **Critical** (Page immediately):
   - API error rate > 5%
   - Database connection failures
   - Payment processing failures
   - Security breaches

2. **Warning** (Notify in business hours):
   - Response time degradation
   - Scraper failure rate > 10%
   - Queue backlog growing
   - Cache miss rate increasing

3. **Info** (Log only):
   - Deployment events
   - Configuration changes
   - Unusual traffic patterns

## Disaster Recovery

### Backup Strategy

1. **Database**: Continuous WAL archiving + daily full backups
2. **File Storage**: S3 versioning + cross-region replication
3. **Configuration**: GitOps with sealed secrets
4. **Recovery Time Objective (RTO)**: < 4 hours
5. **Recovery Point Objective (RPO)**: < 1 hour

### Failover Plan

1. **Multi-AZ Deployment**: Database and critical services
2. **Health Checks**: Automatic instance replacement
3. **Traffic Shifting**: Gradual rollback on deployment failures
4. **Manual Override**: Kill switches for features

---

This architecture document serves as the foundation for implementation. Each section will be realized through production-grade code in subsequent phases.
