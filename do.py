import json
from typing import Dict, List, Union, Any
from aiogram import types


async def do_remember_user_start(message: types.Message) -> bool:
    try:
        with open("users.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            
            if str(message.chat.id) not in data["users"].keys():
                new_user = {
                    "username": message.from_user.username,
                    "first_last": message.from_user.first_name + " " + message.from_user.last_name
                }

                data["users"][message.chat.id] = new_user

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
            file.truncate()

        return True
    except:
        return False