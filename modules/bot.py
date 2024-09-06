from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Funcs:
    @classmethod
    def creating_invite_link(cls, user_id: int, bot_username: str) -> str:
        invite_link = f'https://t.me/{bot_username}?start={str(user_id)}'
        return invite_link
        
    @classmethod
    def menu(cls):
        kb = [
            [
                KeyboardButton(text='🔑 Account'),
            ],
        ]
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )
        
        return keyboard

