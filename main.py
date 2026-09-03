from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from models import RootResponse, HealthResponse
from routes.ask import router as ask_router

app = FastAPI(
    title="The Worst Advice Committee API",
    description="നിങ്ങളുടെ പ്രശ്നം. ഞങ്ങളുടെ മൂന്ന് വിദഗ്ധർ. ഉപദേശം മാത്രം മോശം.",
    version="1.0.0",
)

# Enable CORS for frontend Vite application
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(ask_router)


@app.get("/", response_model=RootResponse, tags=["General"])
async def root():
    return {"message": "Worst Advice Committee backend is alive 💀"}


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health():
    return {"status": "ok"}