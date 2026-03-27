 # CI/CD Pipeline Project

Automated CI/CD pipeline with multi-environment deployment and quality gates.

## Overview
This project demonstrates DevOps practices using GitHub Actions, Docker, and security scanning.

## Features
- Flask REST API with `/health` and `/api/items` endpoints
- Automated testing with pytest (80%+ coverage requirement)
- Docker containerization with multi-stage builds
- GitHub Actions CI/CD with 4 sequential stages
- Trivy security scanning (blocks HIGH/CRITICAL vulnerabilities)
- Docker Hub integration

## Tech Stack
- Python 3.13 + Flask
- pytest + pytest-cov
- Docker
- GitHub Actions
- Trivy
- Docker Hub

## Local Development

### Setup
```bash
pip install -r requirements.txt
pytest src/ --cov
python src/app.py
```

### Docker
```bash
docker build -t ci-cd-api .
docker run -p 5000:5000 ci-cd-api
curl http://localhost:5000/health
```

## CI/CD Pipeline

### Workflow Stages
1. **Build** - Docker image creation
2. **Test** - pytest with coverage verification (≥80%)
3. **Scan** - Trivy security scanning
4. **Push** - Docker Hub deployment (if all pass)

## Project Status
✅ Phase 1: Complete
✅ Phase 2: Complete (CI Pipeline with quality gates)
