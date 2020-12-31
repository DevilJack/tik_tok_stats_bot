from configparser import ConfigParser
from keyboards import ListOfButtons


config = ConfigParser()
config.read("config.ini")

TOKEN = config['tokens']['TOKEN']

ROLES_KEYBOARD = ListOfButtons(
    text = [
        'Админ', 
        'Участник'
    ],
    callback=['admin', 'user'],
    align=[1, 1]
).inline_keyboard

# SUB_CHANNEL_KEYBOARD = ListOfButtons(
#     text = [
#         'Подписаться',
#         "Я подписан"
#     ],
#     callback=['to_sub', 'sub_first'],
#     align=[1, 1],
#     url = ["http://t.me/zhozh_stefanie_bot", None]
# ).inline_keyboard