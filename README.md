# CI/CD Pipeline Project

Automated CI/CD pipeline with multi-environment deployment, quality gates, and rollback capability.

## Project Overview

This project demonstrates production-grade DevOps practices using GitHub Actions, Docker, security scanning, and automated deployment to Railway.app. The pipeline enforces quality gates at multiple stages and provides reliable rollback mechanisms.

**Key Features:**
- ✅ RESTful Task Management API with authentication
- ✅ User registration and JWT-based auth
- ✅ Full CRUD operations on tasks
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Automated CI/CD with 4-stage pipeline
- ✅ Container-based testing for environment parity
- ✅ Security scanning with Trivy
- ✅ Multi-environment deployment (dev/prod)
- ✅ Automated rollback capability (<2 minutes average)
- ✅ 80%+ test coverage with 23 comprehensive tests

---

## Tech Stack

### Application
- **Language:** Python 3.13
- **Framework:** Flask 3.0.0
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** JWT (Flask-JWT-Extended)
- **Password Hashing:** Bcrypt
- **Testing:** pytest 7.4.3 + pytest-cov 4.1.0

### DevOps Tools
- **Containerization:** Docker (multi-stage builds)
- **CI/CD Platform:** GitHub Actions
- **Security Scanner:** Trivy
- **Container Registry:** Docker Hub
- **Deployment Platform:** Railway.app
- **Version Control:** Git + GitHub

---

## Architecture

### CI/CD Pipeline Flow
```
Developer Push → GitHub
       ↓
GitHub Actions CI Pipeline
       ↓
   ┌───────┬────────┬──────────┬─────────┐
   │ Build │  Test  │   Scan   │  Push   │
   │Docker │pytest  │  Trivy   │Docker   │
   │ Image │80% cov │HIGH/CRIT │  Hub    │
   └───┬───┴────┬───┴─────┬────┴────┬────┘
       ✓        ✓         ✓         ✓
              All Pass?
               /     \
             Yes      No (Block)
              ↓
        Docker Hub Storage
              ↓
      ┌───────┴────────┐
      ↓                ↓
 Deploy Dev      Deploy Prod
 (Auto on dev)   (Manual approval)
 Railway.app     Railway.app
      ↓                ↓
 Health Check    Health Check
```

### Rollback Flow
```
Issue Detected → Trigger Rollback Workflow
                        ↓
           Specify: Environment + Image Tag
                        ↓
                Manual Approval (if prod)
                        ↓
           Pull Specific Image from Docker Hub
                        ↓
              Railway Auto-Redeploys
                        ↓
                  Health Check
                        ↓
               Service Restored (~1 min)
```

---

## API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy"}
```

### Authentication

#### Register User
```bash
POST /api/auth/register
Body: {
  "username": "john",
  "email": "john@example.com",
  "password": "secure123"
}
Response: {
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "created_at": "2026-04-01T10:30:00"
}
```

#### Login
```bash
POST /api/auth/login
Body: {
  "username": "john",
  "password": "secure123"
}
Response: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Task Management (Requires Authentication)

#### Get All Tasks
```bash
GET /api/tasks
Headers: Authorization: Bearer <token>
Query Params: ?status=todo&priority=high&category=work
Response: [
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish CI/CD implementation",
    "status": "in_progress",
    "priority": "high",
    "category": "work",
    "due_date": "2026-04-10T00:00:00",
    "created_at": "2026-04-01T10:00:00",
    "updated_at": "2026-04-01T14:30:00",
    "user_id": 1
  }
]
```

#### Create Task
```bash
POST /api/tasks
Headers: Authorization: Bearer <token>
Body: {
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "status": "todo",
  "category": "personal",
  "due_date": "2026-04-05T18:00:00"
}
Response: { task object }
```

#### Get Single Task
```bash
GET /api/tasks/{id}
Headers: Authorization: Bearer <token>
Response: { task object }
```

#### Update Task
```bash
PUT /api/tasks/{id}
Headers: Authorization: Bearer <token>
Body: {
  "status": "done",
  "priority": "low"
}
Response: { updated task object }
```

#### Delete Task
```bash
DELETE /api/tasks/{id}
Headers: Authorization: Bearer <token>
Response: {"message": "Task deleted"}
```

### Task Properties
- **title** (required): Task name
- **description** (optional): Task details
- **status** (optional): `todo`, `in_progress`, `done` (default: `todo`)
- **priority** (optional): `low`, `medium`, `high` (default: `medium`)
- **category** (optional): Custom category tag
- **due_date** (optional): ISO format datetime

---

## Local Development

### Prerequisites
- Python 3.10+
- Docker Desktop
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/styl3s/ci-cd-project.git
cd ci-cd-project

# Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
pytest src/test_app.py --cov=src --cov-report=term

# Run application
python src/app.py
# Visit: http://localhost:5000/health
```

### Docker
```bash
# Build image
docker build -t ci-cd-api:local .

# Run container
docker run -p 5000:5000 ci-cd-api:local

# Test
curl http://localhost:5000/health
```

---

## CI/CD Workflows

### 1. CI Pipeline (Automatic)
**Trigger:** Push or PR to main/dev branches

**Stages:**
1. **Build** - Multi-stage Docker image creation
2. **Test** - pytest execution with 80% coverage threshold
3. **Scan** - Trivy security scanning (blocks HIGH/CRITICAL)
4. **Push** - Docker Hub deployment (only if all pass)

**Average time:** ~4 minutes

### 2. Deploy to Development (Automatic)
**Trigger:** Push to dev branch

**Actions:**
- Validates deployment
- Railway auto-deploys latest image
- Runs health checks

**Average time:** ~45 seconds

### 3. Deploy to Production (Manual)
**Trigger:** Manual workflow dispatch

**Actions:**
- Requires manual approval
- Railway deploys specified image tag
- Runs health checks

**Average time:** ~1 minute (+ approval time)

### 4. Rollback (Manual)
**Trigger:** Manual workflow dispatch

**Parameters:**
- Environment (dev/prod)
- Image tag (commit SHA)

**Actions:**
- Validates image exists
- Triggers Railway redeployment
- Confirms via health check

**Average time:** 1m 4s

---

## Deployment Environments

### Development
- **URL:** https://api-production-3ebb.up.railway.app
- **Branch:** dev
- **Deployment:** Automatic on push
- **Purpose:** Integration testing

### Production
- **URL:** https://api-production-bb06.up.railway.app
- **Branch:** main
- **Deployment:** Manual with approval
- **Purpose:** End-user service

---

## Project Metrics

### CI Pipeline Performance
- **Total commits tested:** 20+
- **Quality gate effectiveness:** 100%
- **Test failures caught:** 2/2
- **Coverage drops caught:** 1/1
- **Vulnerabilities blocked:** 2/2
- **Average pipeline time:** 4m 15s

### Deployment Reliability
- **Total deployments:** 3+ verified
- **Success rate:** 100% (valid configs)
- **Average deployment time:** 45s
- **Health check accuracy:** 100%

### Rollback Capability
- **Total rollback tests:** 5
- **Success rate:** 100% (5/5)
- **Average rollback time:** 1m 4s
- **Fastest rollback:** 59s
- **Target met:** ✅ All under 5 minutes

### Code Quality
- **Test coverage:** 80%+ (target met)
- **Number of tests:** 23
- **API endpoints:** 9
- **Database models:** 2 (User, Task)
- **Production vulnerabilities:** 0 HIGH/CRITICAL

---

## Documentation

- **[TESTING.md](TESTING.md)** - 10 experimental commits validating quality gates
- **[DEPLOYMENT_LOG.md](Deployment_log.md)** - Deployment testing results
- **[ROLLBACK_TESTS.md](ROLLBACK_TESTS.md)** - Rollback validation (5 scenarios)
- **[METRICS.md](METRICS.md)** - Complete project metrics and statistics

---

## Project Structure
```
ci-cd-project/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline
│       ├── deploy-dev.yml      # Dev deployment
│       ├── deploy-prod.yml     # Prod deployment
│       └── rollback.yml        # Rollback workflow
├── src/
│   ├── app.py                  # Flask application
│   └── test_app.py             # pytest test suite
├── docker-compose.dev.yml      # Dev environment config
├── docker-compose.prod.yml     # Prod environment config
├── Dockerfile                  # Multi-stage build
├── requirements.txt            # Python dependencies
├── TESTING.md                  # Quality gate validation
├── DEPLOYMENT_LOG.md           # Deployment testing
├── ROLLBACK_TESTS.md           # Rollback validation
└── README.md                   # This file
```

---

## Success Criteria Met

### Phase 1: Application and Container Baseline
- [x] Flask app with /health and /api/items endpoints
- [x] Test suite with 95%+ coverage
- [x] Docker containerization
- [x] GitHub version control

### Phase 2: CI and Quality Gates
- [x] 4-stage automated pipeline
- [x] Test coverage enforcement (80% threshold)
- [x] Security scanning (Trivy)
- [x] 10 experimental commits validated
- [x] Automated Docker Hub deployment

### Phase 3: Multi-Environment Deployment
- [x] Separate dev/prod configurations
- [x] Automated dev deployment
- [x] Manual prod deployment with approval
- [x] Health checks implemented
- [x] 95%+ deployment success rate

### Phase 4: Rollback and Documentation
- [x] Rollback workflow implemented
- [x] 5 rollback tests (100% success)
- [x] Average rollback time: 1m 4s
- [x] Comprehensive documentation
- [x] Architecture diagrams

## Live Demo - Presentation
- Automated CI/CD Pipeline
- Date: April 1, 2026
- For Presentaion purpose

## Live Demo - Presentation Live Demo
- Automated CI/CD Pipeline
- Date: April 1, 2026
- For Presentaion purpose