import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse

from app.manager.config import ConfigManager

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self , request , call_next):

        if request.url.path.startswith('/api') and not request.url.path.startswith('/api/notification/stream/') :
            short_id = uuid.uuid4().hex[:8]
            request_body = await request.body()
            
            LoggerManager.info(f'{short_id} Request URL: {request.url}')
            LoggerManager.info(f'{short_id} Request method: {request.method}')
            LoggerManager.info(f'{short_id} Request headers: {request.headers}')
            LoggerManager.info(f'{short_id} Request from IP: {request.client.host}')
            LoggerManager.info(f'{short_id} Request body: {request_body.decode("utf-8")}')

            request = Request(request.scope, receive=lambda: {'type': 'http.request', 'body': request_body})
            response = await call_next(request)

            response_body = [chunk async for chunk in response.body_iterator]
            response_text = b''.join(response_body).decode('utf-8')
            LoggerManager.info(f'{short_id} Response status code: {response.status_code}')
            LoggerManager.info(f'{short_id} Response body: {response_text}')

            return PlainTextResponse(content=response_text, status_code=response.status_code, headers=dict(response.headers))
        return await call_next(request)


class LoggerManager:
    _logging_instance = None
    _scheduler_logging_instance = None

    @classmethod
    def init_logger(cls) -> None:
        logger_level = cls.get_logger_level(ConfigManager.get_config().logger_level)

        file_handler = logging.FileHandler(ConfigManager.get_config().logger_path)
        file_handler.setLevel(logger_level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_level)
        
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        if cls._logging_instance is None:
            cls._logging_instance = logging.getLogger()
            cls._logging_instance.setLevel(logger_level)
            
            cls._logging_instance.addHandler(file_handler)
            cls._logging_instance.addHandler(console_handler)

        if cls._scheduler_logging_instance is None:
            cls._scheduler_logging_instance = logging.getLogger('apscheduler')
            cls._scheduler_logging_instance.setLevel(logger_level)
            cls._scheduler_logging_instance.addHandler(file_handler)
            cls._scheduler_logging_instance.addHandler(console_handler)

    @classmethod
    def get_logger_level(cls, level: str) -> int:
        if level.lower() == 'debug':
            return logging.DEBUG
        if level.lower() == 'info':
            return logging.INFO
        if level.lower() == 'warning':
            return logging.WARNING
        if level.lower() == 'error':
            return logging.ERROR
        return logging.INFO

    @classmethod
    def debug(cls, log: str) -> None:
        cls._logging_instance.debug(log)

    @classmethod
    def info(cls, log: str) -> None:
        cls._logging_instance.info(log)

    @classmethod
    def warning(cls, log: str) -> None:
        cls._logging_instance.warning(log)

    @classmethod
    def error(cls, log: str) -> None:
        cls._logging_instance.error(log)
    
    @classmethod
    def close_logger(cls) -> None:
        if cls._scheduler_logging_instance is not None:
            cls._logging_instance = None
        if cls._scheduler_logging_instance is not None:
            cls._logging_instance = None