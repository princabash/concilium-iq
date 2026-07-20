"""
Concilium IQ™ — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, patients, labs, summary, risk, care_gaps, actions
from app.config import settings

app = FastAPI(
    title="Concilium IQ™",
    description="AI-powered Clinical Intelligence Platform for Cardiovascular Risk Assessment",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(labs.router, prefix="/api/v1/labs", tags=["Lab Results"])
app.include_router(summary.router, prefix="/api/v1/summary", tags=["Patient Summary"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risk Assessment"])
app.include_router(care_gaps.router, prefix="/api/v1/care-gaps", tags=["Care Gaps"])
app.include_router(actions.router, prefix="/api/v1/actions", tags=["Suggested Actions"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Concilium IQ™",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "concilium-iq-backend"}
