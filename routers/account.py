from aiogram import Router, F
from aiogram.types import Message
from loguru import logger

from modules.users import Users
from modules.bot import Funcs

account = Router()

@account.message(F.text=='🔑 Account')
async def _account(message: Message) -> None:
    answer = ''
    user_id = message.from_user.id

    with Users() as module:
        select_user_info_response = await module.select_user_info(user_id)
        
    if select_user_info_response['status'] == 'error':
        answer = select_user_info_response['err_description']
    else:
        user = select_user_info_response['user']
        answer = f'Fullname: <b>{user.user_fullname}</b>\n' \
          f'Balance: <b>{user.balance}</b>\n' \
          f'Referral link: <b>{user.referral_link}</b>\n' \
          f'Created: <b>{user.created_at}</b>'
          
    await message.reply(answer, reply_markup=Funcs.menu(), parse_mode='HTML')
