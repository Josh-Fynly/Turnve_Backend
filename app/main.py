"""
TURN - Project Manager Career Platform
FastAPI main application with PostgreSQL backend.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes import routers
from app.core.logging_middleware import RequestLoggingMiddleware, DatabaseQueryLoggingMiddleware

EXPORT_ROOT = Path(__file__).resolve().parent.parent / "exports"
EXPORT_ROOT.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("=" * 80)
    print(f" Starting {settings.app_name}")
    print(f" Environment: {settings.environment}")
    print(f" Debug mode: {settings.debug}")
    print("=" * 80)
    
    yield
    
    # Shutdown
    print("=" * 80)
    print(f" Shutting down {settings.app_name}")
    print("=" * 80)


def custom_openapi():
    """
    Custom OpenAPI schema with OAuth2 password flow for Swagger UI.
    This allows users to login with email/password directly in Swagger.
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Configure OAuth2 password flow for Swagger UI authentication
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {}
                }
            },
            "description": "Login with your email and password. Your role is automatically included in the token."
        }
    }
    
    # Set default security to OAuth2 ONLY
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    TURNVE - A comprehensive web application for aspiring project managers.
    
    ##  How to Authenticate
    
    **Simple 3-Step Login:**
    
    1. **Click "Authorize" ** (green button at top right)
    2. **Enter your credentials:**
       - Username: `your-email@example.com`
       - Password: `your-password`
    3. **Click "Authorize"** - Done! All requests now authenticated
    
    **No Bearer tokens to copy!** The token is handled automatically.
    
    ---
    
    ##  Role-Based Access Control (RBAC)
    
    -  **USER**: Regular job seekers and learners (default)
    -  **RECRUITER**: Can post jobs and manage applications
    -  **COMPANY**: Company representatives with extended access
    -  **MENTOR**: Provides mentorship and guidance
    -  **ADMIN**: Platform administrators with full access
    
    Your role determines which endpoints you can access.
    
    --- Features
    
    * **User Management** - Registration, authentication, and profile management
    * **AI PM Teacher** - Intelligent coaching, personalized learning paths, and career guidance
    * **Project Management** - Complete project lifecycle with AI coaching
    * **CV Builder** - Dynamic resume creation with export functionality
    * **Job Search** - Job listings, applications, and recommendations
    * **Learning Hub** - Courses from top platforms like Coursera, edX, YouTube
    * **Project Simulations** - Real-world case studies from Netflix, Spotify, Tesla
    * **Portfolio Builder** - Showcase your PM projects and achievements
    * **Direct Application** - AI-powered direct application to CEO/HR of startups and SMEs
    
    ## AI-Powered Learning
    
    * **Personalized Learning Paths** - 12-week customized programs based on your level
    * **AI Coaching Sessions** - One-on-one mentorship with expert AI PM teacher
    * **Scenario Analysis** - Get feedback on your PM decisions and strategies
    * **Interview Preparation** - Practice with AI-generated interview questions
    * **Career Guidance** - Personalized advice for PM career advancement
    

    """,
    version="1.0.0",
    contact={
        "name": "TURNVE Development Team",
        "email": "supporttech@turnve.com",
    },

    lifespan=lifespan,
    debug=settings.debug,
    
    # Configure Swagger UI settings
    swagger_ui_parameters={
        "persistAuthorization": True,  # Remember auth between page refreshes
        "displayRequestDuration": True,  # Show request time
        "filter": True,  # Enable search/filter
        "tryItOutEnabled": True,  # Enable "Try it out" by default
    }
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Add logging middleware (add FIRST for most accurate timing)
if settings.debug:
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(DatabaseQueryLoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://turn-platform.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["turn-platform.com", "*.turn-platform.com"]
    )

# Include all routers
for router in routers:
    app.include_router(router, prefix="/api/v1")

# Static exports directory
app.mount("/exports", StaticFiles(directory=str(EXPORT_ROOT)), name="exports")


# Health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment,
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )