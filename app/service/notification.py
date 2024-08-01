from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import async_timeout

from app.service.service import bindResponse
from app.model.error import InternalServerError
from app.model.notification import PublishRequest
from app.manager.logger import LoggerManager
from app.manager.cache import RedisManager

router = APIRouter()
    
@router.get('/api/notification/stream/{user_id}',
            summary = "start sse notification",
            description= "start sse notification")
async def notification_sse(user_id: str):
    try:
        return EventSourceResponse(subscribe(user_id))
    
    except Exception as e:
        LoggerManager.error(f"start sse notification error, error message:{e}")
        return bindResponse(InternalServerError())

async def subscribe(user_id: str):
    channel = f"user_{user_id}_channel"
    pubsub = RedisManager.get_redis().pubsub()
    await pubsub.subscribe(channel)

    try:
        max_retries = 100
        retries = 0
        while retries < max_retries:
            try:
                async with async_timeout.timeout(1):
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:
                        yield {"event": "message", "data": message["data"].decode()}
            except asyncio.TimeoutError:
                retries += 1
            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()

@router.post('/api/notification/publish/{user_id}',
            summary = "publish message",
            description= "publish message")
async def publish(user_id: str, request: PublishRequest):
    try:
        channel = f"user_{request.friend_id}_channel"
        message = f"User {user_id} has posted a new message!"
        await RedisManager.get_redis().publish(channel=channel, message=message)
        return JSONResponse(status_code=200, content={"message": "Message published"})
    
    except Exception as e:
        LoggerManager.error(f"publish message error, error message:{e}")
        return bindResponse(InternalServerError())

@router.get("/page/notification", response_class=HTMLResponse)
def get_upload_page():
    with open("app/static/notification.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

