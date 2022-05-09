
import nest_asyncio
nest_asyncio.apply()

import ParserClass, config, asyncio, utils, pretty, Logic
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link, bold, underline

parser = ParserClass.HuinyaParser()

logs_chat = pretty.logs
goods_chat = pretty.goods

TOK = pretty.token

bot = Bot(token=TOK)
dp = Dispatcher(bot)

@dp.message_handler(commands=['test'])
async def testtt(message: types.Message):
    await Logic.worker_many(bot)

@dp.message_handler(commands=['testtest'])
async def testtt(message: types.Message):
    await Logic.worker_one(bot)

@dp.message_handler(commands=['thread'])
async def testtt(message: types.Message):
    itid = 1
    while True:
        item = parser.buff_first_item()
        print(item, itid)
        if item != itid:
            itid = item
            await Logic.worker_one(bot, item)
        await asyncio.sleep(30)

@dp.callback_query_handler(lambda c: c.data == 'delete_this_shit')
async def delete_shit(c: types.CallbackQuery):
    await bot.delete_message(c.message.chat.id, c.message.message_id)
    await bot.answer_callback_query(c.id)

# @dp.message_handler(filters.ChatTypeFilter(types.ChatType.GROUP) | filters.ChatTypeFilter(types.ChatType.SUPERGROUP))
# async def tess(message: types.Message):
#     # print(message)
#     await bot.send_message(
#         "-1001509146655", 
#         message_text,
#         parse_mode=types.ParseMode.MARKDOWN
#     )
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)