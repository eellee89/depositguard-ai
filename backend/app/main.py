from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import cases, agent

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered security deposit dispute resolution for Texas tenants",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(agent.router, prefix="/api/agent", tags=["Agent"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print(f"🚀 Starting {settings.APP_NAME}...")
    print(f"📊 Initializing database...")
    init_db()
    print(f"✅ Database initialized")
    print(f"🤖 Claude model: {settings.CLAUDE_MODEL}")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
