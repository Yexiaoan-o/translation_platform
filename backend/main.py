from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import projects, translation, terminology, documents

app = FastAPI(
    title="Translation Platform API",
    description="API for the online translation platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Translation Platform API"}

# Include routers
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(translation.router, prefix="/api/translation", tags=["translation"])
app.include_router(terminology.router, prefix="/api/terminology", tags=["terminology"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])