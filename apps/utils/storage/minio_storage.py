from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MinIOStorage(S3Boto3Storage):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("endpoint_url", settings.MINIO_ENDPOINT_URL)
        kwargs.setdefault("access_key", settings.MINIO_ACCESS_KEY)
        kwargs.setdefault("secret_key", settings.MINIO_SECRET_KEY)
        kwargs.setdefault("bucket_name", settings.MINIO_BUCKET_NAME)
        kwargs.setdefault("region_name", "us-east-1")  # required by boto3; ignored by MinIO
        kwargs.setdefault("use_ssl", getattr(settings, "MINIO_USE_SSL", False))
        kwargs.setdefault("querystring_auth", getattr(settings, "MINIO_PRESIGNED_URLS", True))
        kwargs.setdefault("file_overwrite", False)
        super().__init__(*args, **kwargs)
