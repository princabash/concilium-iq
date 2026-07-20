# 🧠 Concilium IQ™

> AI-powered Clinical Intelligence Platform for Cardiovascular Risk Assessment

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

Concilium IQ™ is a comprehensive clinical intelligence platform designed to:
- Assess cardiovascular risk using evidence-based clinical guidelines
- Generate intelligent patient summaries with actionable care gaps
- Provide explainable AI recommendations for clinicians
- Track lab results and therapy progress over time

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React + Vite  │────▶│   FastAPI       │────▶│   PostgreSQL    │
│   Tailwind CSS  │◄────│   (Python 3.11) │◄────│   (Async SQLAlchemy)
│   React Query   │     │                 │     │                 │
│   Zustand       │     │   Risk Engine   │     │   Neo4j         │
└─────────────────┘     │   Rule Engine   │     │   (Graph DB)    │
                        │   Explainability│     │                 │
                        └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │   Redis (Cache) │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/concilium-iq.git
cd concilium-iq
```

### 2. Start all services

```bash
docker-compose up --build
```

### 3. Access the application

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:3000 |
| Patient Portal | http://localhost:3001 |
| API Docs | http://localhost:8000/docs |
| API (Redoc) | http://localhost:8000/redoc |
| Neo4j Browser | http://localhost:7474 |
| Nginx Proxy | http://localhost |

### 4. Run tests

```bash
docker-compose exec backend pytest app/tests/ -v
```

### 5. Seed test data

```bash
docker-compose exec backend python scripts/seed_data.py
```

## 📁 Project Structure

```
concilium-iq/
├── docker-compose.yml          # 7 services orchestration
├── backend/
│   ├── Dockerfile              # Python 3.11 + Poetry
│   ├── pyproject.toml          # Dependencies
│   ├── alembic.ini             # DB migrations
│   └── app/
│       ├── main.py             # FastAPI app entry
│       ├── config.py           # Pydantic settings
│       ├── api/v1/             # 7 API routers
│       ├── core/               # Risk, Rule, Explainability engines
│       ├── db/                 # Async SQLAlchemy setup
│       ├── models/             # Patient, LabResult ORM
│       ├── schemas/            # Pydantic models
│       ├── services/           # Business logic layer
│       ├── graph/              # Neo4j client + seed data
│       └── tests/              # 12 test cases
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── Layout/
│       ├── Pages/
│       ├── Components/
│       ├── Hooks/
│       └── Store/              # Zustand state management
├── patient-portal/             # Next.js patient-facing app
│   ├── Dockerfile
│   └── src/
├── infrastructure/
│   └── docker/
│       ├── nginx/
│       │   └── nginx.conf      # Reverse proxy config
│       └── postgres/
│           └── init.sql        # DB extensions
├── scripts/
│   └── seed_data.py            # Test data generator
├── .gitignore
├── README.md
└── LICENSE
```

## 🔧 Development

### Backend (without Docker)

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### Frontend (without Docker)

```bash
cd frontend
npm install
npm run dev
```

### Patient Portal (without Docker)

```bash
cd patient-portal
npm install
npm run dev -- --port 3001
```

## 🧪 Test Data

The project includes 3 test patients with realistic clinical data:
- **Very High Risk** — ASCVD patient with multiple risk factors
- **High Risk** — Diabetic patient with dyslipidemia
- **Low Risk** — Healthy control patient

Load them via: `docker-compose exec backend python scripts/seed_data.py`

## 🛡️ Core Engines

| Engine | Purpose |
|--------|---------|
| **Risk Engine™** | Calculates cardiovascular risk scores (ASCVD, SCORE2, QRISK) |
| **Rule Engine™** | Applies clinical guidelines (ACC/AHA, ESC/EAS) |
| **Explainability Engine™** | Generates human-readable rule traces and confidence scores |

## 📚 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/login` | JWT authentication |
| `GET /api/v1/patients` | List patients |
| `GET /api/v1/patients/{id}/summary` | Full clinical summary |
| `GET /api/v1/patients/{id}/risk` | Risk assessment |
| `GET /api/v1/patients/{id}/care-gaps` | Identified care gaps |
| `POST /api/v1/labs` | Submit lab results |
| `GET /api/v1/actions` | Suggested clinical actions |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ACC/AHA Guidelines for Cardiovascular Risk Assessment
- ESC/EAS Guidelines for Dyslipidemia Management
- FastAPI & React communities

---

<p align="center">
  <sub>Built with ❤️ for better patient outcomes</sub>
</p>
