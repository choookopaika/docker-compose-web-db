import logging
import psycopg2
from psycopg2 import Error
from fastapi import FastAPI

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.get("/")
def root():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute("INSERT INTO visits DEFAULT VALUES")
        connection.commit()

        cursor.execute("SELECT COUNT(*) FROM visits")
        count = cursor.fetchone()[0]

        logger.info("Успешный запрос. Визитов: %s", count)
        return f"Hello! I have been visited {count} times"

    except (Exception, Error) as error:
        logger.error("Ошибка при работе с PostgreSQL: %s", error)
        return "Database error"

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
