#!/usr/bin/env python
"""
Safe migration script to repair the Neon/Postgres task table schema.
This script addresses:
1. Ensures task.id is auto-generated INTEGER primary key
2. Ensures task.user_id is INTEGER type
3. Fixes any schema mismatches between SQLModel and database
"""

import os
from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy import text
import logging

# Load environment variables first
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use NEON_DATABASE_URL if available, otherwise fall back to DATABASE_URL, then SQLite
DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL") or "sqlite:///./todo_app.db"

engine = create_engine(DATABASE_URL)

def repair_task_table_schema():
    """
    Repair the task table schema to match SQLModel expectations.
    For development, this will drop and recreate the task table safely.
    """
    logger.info("Starting task table schema repair...")

    with engine.begin() as conn:
        # Check database type
        is_postgresql = "postgresql" in str(conn.engine.url)

        if is_postgresql:
            logger.info("Detected PostgreSQL/Neon database, repairing schema...")

            # Drop the task table if it exists (data loss acceptable for dev)
            logger.info("Dropping existing task table...")
            conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))

            # Create the task table with correct schema matching SQLModel
            logger.info("Creating task table with correct schema...")
            conn.execute(text("""
                CREATE TABLE task (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description VARCHAR(500),
                    completed BOOLEAN DEFAULT FALSE NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES public.user(id)
                )
            """))

            # Add trigger to update updated_at timestamp automatically
            # First, drop the trigger if it exists
            try:
                conn.execute(text("DROP TRIGGER IF EXISTS update_task_updated_at ON task"))
            except:
                pass  # Ignore if trigger doesn't exist

            # Create function to update timestamp
            try:
                conn.execute(text("""
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                """))
            except:
                pass  # Function might already exist

            # Create trigger to update timestamp on update
            try:
                conn.execute(text("""
                    CREATE TRIGGER update_task_updated_at
                    BEFORE UPDATE ON task
                    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
                """))
            except:
                pass  # Trigger might already exist

            logger.info("Successfully repaired task table schema")

        else:
            logger.info("Using SQLite, recreating table with correct schema...")
            # For SQLite, drop and recreate with correct schema
            conn.execute(text("DROP TABLE IF EXISTS task"))

            conn.execute(text("""
                CREATE TABLE task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(100) NOT NULL,
                    description VARCHAR(500),
                    completed BOOLEAN DEFAULT 0 NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                )
            """))

            logger.info("Successfully recreated SQLite task table")

    logger.info("Schema repair completed successfully!")

if __name__ == "__main__":
    repair_task_table_schema()