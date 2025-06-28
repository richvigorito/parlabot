import os
from storage.local import LocalStorage
from storage.gcs import GCSStorage
from config import settings


def make_storage():
    if settings.STORAGE_DRIVER == "gcs":
        return GCSStorage(bucket_name=settings.GCS_BUCKET)
    return LocalStorage()
