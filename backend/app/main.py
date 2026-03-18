from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import projects, clients

app = FastAPI(title="Freelancer Bot API")

# Enable CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(projects.router, prefix="/api/projects")
app.include_router(clients.router, prefix="/api/clients")

@app.get("/")
def read_root():
    return {"message": "Freelancer Bot API running"}
