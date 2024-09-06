import asyncio
import os
from celery import Celery
from loguru import logger

from modules.users import Users

app = Celery(
    'tasks',
    broker=os.environ.get('REDIS_HOST', 'redis://redis:6379')
)

app.conf.task_queues = {
    'high_priority': {
        'exchange': 'high_priority',
        'routing_key': 'high.#'
    }
}

async def add_bonuse_execute(user_id: int, bonuse: int) -> None:
    with Users() as module:
        add_bonuse_response = await module.add_bonuse(user_id, bonuse)
    
    logger.info(
        add_bonuse_response
    )
    
@app.task
def add_bonuse(user_id: int, bonuse: int) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(add_bonuse_execute(user_id, bonuse))
    loop.close()
