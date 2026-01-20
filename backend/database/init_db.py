import os
from sqlmodel import SQLModel
from database.connection import engine
from app.models import Task
from app.user_models import User


def create_db_and_tables():
    """
    Creates the database tables if they don't exist.
    This function should be called when the application starts.
    If RESET_DB environment variable is set to 'true', drops and recreates only the task table.
    """
    # First, ensure all tables exist normally
    SQLModel.metadata.create_all(engine)

    # Check if RESET_DB is set to 'true'
    reset_db = os.getenv('RESET_DB', 'false').lower() == 'true'

    if reset_db:
        # Drop only the task table if it exists and recreate it
        from sqlalchemy import inspect, text
        inspector = inspect(engine)

        # Check if task table exists
        if 'task' in inspector.get_table_names():
            # Drop the task table
            with engine.connect() as conn:
                trans = conn.begin()
                try:
                    # Use raw SQL for dropping table to avoid issues with SQLModel
                    # Handle different database types appropriately
                    if str(engine.url).startswith("postgresql"):
                        conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
                    elif str(engine.url).startswith("sqlite"):
                        # For SQLite, we need to handle it differently since it doesn't support CASCADE
                        conn.execute(text("DROP TABLE IF EXISTS task"))
                    else:
                        conn.execute(text("DROP TABLE IF EXISTS task"))
                    trans.commit()
                except Exception:
                    trans.rollback()
                    # Table might not exist or other issue, continue anyway

        # Recreate only the task table
        Task.__table__.create(engine, checkfirst=True)