from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks
from app.routes.auth import router as auth_router
from database.init_db import create_db_and_tables


def create_app():
    app = FastAPI(title="Todo API", version="0.1.0")

    # CORS middleware with specific allowed origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create database tables on startup
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    # Include routes
    app.include_router(tasks.router)
    app.include_router(auth_router)

    @app.get("/")
    def read_root():
        return {"message": "Todo API is running!"}

    return app


app = create_app()