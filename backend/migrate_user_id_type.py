#!/usr/bin/env python
"""
Simple migration script to fix user_id column type in task table for PostgreSQL/Neon.
"""

import os
from sqlmodel import create_engine
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL") or "sqlite:///./todo_app.db"

engine = create_engine(DATABASE_URL)

def migrate_user_id_column():
    """
    Migrate user_id column in task table to ensure it's INTEGER type.
    """
    logger.info("Starting user_id column type migration...")

    # Use engine.begin() to handle transactions properly and avoid autobegin conflicts
    with engine.begin() as conn:
        # Check database type
        is_postgresql = "postgresql" in str(conn.engine.url)

        if is_postgresql:
            logger.info("Detected PostgreSQL/Neon database, checking column type...")

            # Check current column type
            result = conn.execute(text("""
                SELECT data_type
                FROM information_schema.columns
                WHERE table_name = 'task'
                AND column_name = 'user_id'
            """)).fetchone()

            if result:
                current_type = result[0]
                logger.info(f"Current user_id column type: {current_type}")

                if current_type.lower() in ['character varying', 'varchar', 'text']:
                    logger.info("Converting user_id column from VARCHAR/TEXT to INTEGER...")

                    # First, ensure all values are numeric by updating non-numeric ones
                    # We'll set non-numeric values to a default user_id (e.g., 1)
                    conn.execute(text("""
                        UPDATE task
                        SET user_id = '1'
                        WHERE user_id !~ '^[0-9]+$'
                    """))

                    # Now alter the column type to INTEGER
                    conn.execute(text("""
                        ALTER TABLE task
                        ALTER COLUMN user_id TYPE INTEGER
                        USING user_id::INTEGER
                    """))

                    # Add foreign key constraint
                    try:
                        conn.execute(text("""
                            ALTER TABLE task
                            ADD CONSTRAINT fk_task_user_id
                            FOREIGN KEY (user_id) REFERENCES public.user(id)
                        """))
                    except Exception as e:
                        logger.warning(f"Could not add foreign key constraint: {e}")

                    logger.info("Successfully migrated user_id column to INTEGER type")
                else:
                    logger.info("Column type is already INTEGER, no migration needed")
            else:
                logger.warning("Could not find user_id column in task table")
        else:
            logger.info("Using SQLite, which handles types differently. Column should already be INTEGER.")

if __name__ == "__main__":
    migrate_user_id_column()