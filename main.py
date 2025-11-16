from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Chatbot Gemini V1",
    description="Api rest para interactuar con el modelo Gemini V1",
    version="1.0.0"
)

app.include_router(router, prefix="/api")