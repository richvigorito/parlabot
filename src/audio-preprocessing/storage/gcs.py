from .base import Storage
from google.cloud import storage as gcs

class GCSStorage(Storage):
    def __init__(self, bucket_name):
        self.client = gcs.Client()
        self.bucket = self.client.bucket(bucket_name)

    def save_file(self, filename, data):
        print(f"Saving file to GCS: {filename}")
        print(f"bucket: {self.bucket.name}")
        # safeguard filename needs to start with a slash
        blob = self.bucket.blob(filename)
        blob.upload_from_string(data)
        return f"/files/{filename}"
        #return f"gs://{self.bucket.name}/{filename}"

    def get_url(self, path):
        return f"https://storage.googleapis.com/{self.bucket.name}/{path}"

