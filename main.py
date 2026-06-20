from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import lead_routes
import uvicorn

app = FastAPI(title="AI Outlook Lead Extractor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lead_routes.router)


@app.get("/")
def home():
    return {"message": "Project 4 Backend is Running on Port 8003"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
