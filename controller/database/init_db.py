import logging

# Import all models
# noinspection PyUnresolvedReferences
from controller import model  # noqa: F401
from controller.database.base_class import Base
from controller.database.session import engine, SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        db.close()


def create_all():
    Base.metadata.create_all(engine)
