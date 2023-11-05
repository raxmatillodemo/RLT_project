import json
from aiogram import types
from loader import dp


from utils.misc.mongo import querResult

# Echo bot


@dp.message_handler(state=None)
async def queryResponse(message: types.Message):
    try:
        res = json.loads(message.text)
        result = querResult(res)
        await message.answer(result)
    except Exception as err:
        await message.answer(
        """Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""
    )
        return

@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(
        """Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""
    )
