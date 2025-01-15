from dotenv import load_dotenv
load_dotenv()

import logging
import logging
import asyncio
import uvicorn
from aiogram import Dispatcher
from _bot import bot
from leads import fastapi_app
from bot import router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('aiogram').setLevel(logging.WARNING)

dp = Dispatcher()
dp.include_router(router)

async def main():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8500, log_level="warning", loop="asyncio")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())
    bot_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(bot_task, server_task)

if __name__ == '__main__':
    asyncio.run(main())