import os
import asyncio
import aiogram
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from modules.users import Users
from modules.env import Env
from modules.bot import Funcs
from modules.tasks import add_bonuse

from routers.account import account

Env.create()
bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def _start(message: Message, command: CommandObject) -> None:
    await message.answer('Waiting, please ... ⏰')
    
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name
    
    from_user_id = command.args
    if from_user_id and str(from_user_id) != str(user_id):
        add_bonuse_response = add_bonuse.apply_async(
            (from_user_id, 10),
            queue='high_priority'
        )
    
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    invite_link = Funcs.creating_invite_link(
        user_id,
        bot_username
    )
    
    with Users() as module:
        save_new_user_response = await module.save_new_user(
            user_id, user_fullname, invite_link
        )
    
    greetings = f'Hello, <b>{user_fullname}</b>!\nYour invite link: <b>{invite_link}</b>'
    if save_new_user_response['status'] != 'success':
        greetings = save_new_user_response['err_description']
    
    await message.answer(greetings, reply_markup=Funcs.menu(), parse_mode='HTML')

async def main() -> None:
    global db, bot
    
    dp.include_router(account)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
        
    except Exception as e:
        logger.error(str(e))
