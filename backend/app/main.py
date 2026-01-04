from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router  # absolute import
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Matcher")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["Resume"])

@app.get("/")
def root():
    return {"message": "AI Resume Matcher API"}
