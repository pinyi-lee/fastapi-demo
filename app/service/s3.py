import boto3

from app.util.config import ConfigManager
from botocore.config import Config

class s3Manager:
    _s3_instance = None

    @classmethod
    def init_s3(cls) -> None:
        if cls._s3_instance is None:
            cls._s3_instance = boto3.client('s3',
                aws_access_key_id=ConfigManager.get_config().aws_access_key_id,
                aws_secret_access_key=ConfigManager.get_config().aws_secret_access_key,
                region_name=ConfigManager.get_config().aws_region,
                config=Config(signature_version='s3v4')
            )
    
    @classmethod
    def get_s3(cls) -> boto3.client:
        return cls._s3_instance
    
    @classmethod
    def close_s3(cls) -> None:
        if cls._s3_instance is not None:
            cls._s3_instance = None