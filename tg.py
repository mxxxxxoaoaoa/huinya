
import nest_asyncio
nest_asyncio.apply()
import re
import os
import utils
import logging
import time
import config 
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import link, bold, underline
import utils

import Logic

logs_chat = config.logs
goods_chat = config.goods

TOK = "5322383577:AAGkYtOKpggmFrCIYakxMcAGD40Alt0srOk"

bot = Bot(token=TOK)
dp = Dispatcher(bot)

@dp.message_handler(commands=['rust'])
async def rust_searcher(message: types.Message):
    prices = [0.28, 0.28, 0.28, 0.28, 0.29, 0.29, 0.29, 0.29, 0.3, 0.3]
    prices1 = [123, 1234, 1234, 12345, 123, 1234, 12345, 123, 1234, 12345]

    buys = [{'price': '3749.5', 'date': '22.04.29'}, {'price': '3998', 'date': '22.04.29'}, {'price': '3998', 'date': '22.04.29'}, {'price': '3250', 'date': '22.04.28'}, {'price': '3800', 'date': '22.04.28'}, {'price': '3800', 'date': '22.04.28'}, {'price': '3480', 'date': '22.04.28'}, {'price': '3470', 'date': '22.04.28'}, {'price': '4200', 'date': '22.04.28'}, {'price': '3763.66', 'date': '22.04.28'}]


    tm_prices = [8.347, 9.299, 9.299, 9.3, 9.739, 10.434, 34.779]

    message_text = ""

    name = "No Mercy Jacket"
    profit = "50"
    link_buff = "http://bufflink.io"
    prices = [16.08, 16.18, 16.18, 16.2, 19.99, 50.0, 50.0] # CNY
    
    # CNY
    buys = [{'price': '16.99', 'date': '22.04.29'}, {'price': '15.9', 'date': '22.04.29'}, {'price': '14.9', 'date': '22.04.29'}, {'price': '14.45', 'date': '22.04.29'}, {'price': '14.8', 'date': '22.04.29'}, {'price': '14.44', 'date': '22.04.29'}, {'price': '14.21', 'date': '22.04.28'}, {'price': '14.11', 'date': '22.04.28'}, {'price': '13.5', 'date': '22.04.28'}, {'price': '12.9', 'date': '22.04.28'}]
    
    link_rust = "http://rust_link.io"
    count = 1
    pokypki = 44
    m = 1.2 # $
    avg = 2.58 # $ 
    mx = 3.13 # $ 
    now = [2.54, 2.54] # $

    message_text = config.template_1.format(
        name,
        profit,
        link_buff,
        len(prices),
        "$, ".join(map(str, utils.converter_currency_cny_usd(prices))),
        "₽, ".join(map(str, utils.converter_currency_cny_rub(prices))),
        utils.generator_buys(buys),
        utils.generator_buys_rub(buys),
        link_rust,
        count,
        pokypki,
        m, avg, mx,
        utils.converter_currency_usd_rub(m), utils.converter_currency_usd_rub(avg), utils.converter_currency_usd_rub(mx),
        now,
        utils.converter_currency_usd_rub(now)

    )


    await message.answer(message_text, parse_mode=types.ParseMode.MARKDOWN)
   


@dp.message_handler(commands=['test'])
async def testtt(message: types.Message):
    await Logic.worker(bot)

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