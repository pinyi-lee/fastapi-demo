import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse

logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , filename= 'app.log')

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self , request , call_next):
        short_id = uuid.uuid4().hex[:8]
        request_body = await request.body()
        
        logging.info(f'{short_id} Request URL: {request.url}')
        logging.info(f'{short_id} Request method: {request.method}')
        logging.info(f'{short_id} Request headers: {request.headers}')
        logging.info(f'{short_id} Request from IP: {request.client.host}')
        logging.info(f'{short_id} Request body: {request_body.decode("utf-8")}')

        request = Request(request.scope, receive=lambda: {'type': 'http.request', 'body': request_body})
        response = await call_next(request)

        response_body = [chunk async for chunk in response.body_iterator]
        response_text = b''.join(response_body).decode('utf-8')
        logging.info(f'{short_id} Response status code: {response.status_code}')
        logging.info(f'{short_id} Response body: {response_text}')

        return PlainTextResponse(content=response_text, status_code=response.status_code, headers=dict(response.headers))
