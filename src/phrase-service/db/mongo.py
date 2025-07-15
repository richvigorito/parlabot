from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
import logging


logger = logging.getLogger("phrase-service")

try:
    logger.info(f"❌ MONGO_URL: {settings.MONGO_URL}")
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]
    collection = db[settings.COLLECTION_NAME]
except Exception as e:
    logger.info(f"❌ db conn failure: {e}")
