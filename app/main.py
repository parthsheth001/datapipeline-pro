from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DataPipeline Pro",
    description="Real-time Data Processing & Analytics Platform",
    version="0.1.0"
)

#CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {
        "message":"Welcome to DataPipeline Pro",
        "status":"running",
        "version":"0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status":"healthy"}