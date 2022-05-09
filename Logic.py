from datetime import datetime
from ParserClass import HuinyaParser
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import link, bold, underline
import utils, config
from aiogram import types
import urllib.parse
import keyboards as kb
import pretty

parser = HuinyaParser()


def margin(tm, buff):
    margin = ((tm - buff) / tm) * 100
    return round(margin, 2)

def steam_margin(buff, steam):
    s = steam - (steam * 0.3)
    margin = ((s - buff) / s) * 100
    return round(margin, 2 )

async def worker_one(bot, item):
    try:
        data = parser.buff_rust_price_one()
    except:
        await bot.send_message(
            pretty.goods, 
            "куки ёбнули",
            reply_markup = kb.good_kb(),
            parse_mode=types.ParseMode.MARKDOWN
            )
    buff_link = "https://buff.163.com/goods/{}?from=market#tab=selling".format(item)

    name = data['name']
    prices = data['prices']
    buys = parser.buff_buyers(item)
    message_text = ""
    print(data)
    market_data = parser.market_rust_all(data['name'])
    print(market_data)
    print(len(market_data))
    if len(market_data) > 0:
        print('len > 0')
        link = market_data[0]['link']
        try:
            extend = parser.market_rust_extended(link)
        except:
            await bot.send_message(
                pretty.goods, 
                "НАС ТРАХНУЛ РАСТ.ТМ. ПИДАРАСЫ?",
                reply_markup = kb.good_kb(),
                parse_mode=types.ParseMode.MARKDOWN)
            
        counts = len(market_data)
        pokypki = extend['buys']
        m = extend['min_price']
        avg = extend['averange'],
        mx = extend['max_price']
        now = extend['prices']
        ab_all = extend['autobuy']['all']
        autobuy_dollars = extend['autobuy']['requests']
        try:
            print(prices[0])
            profit = margin(now[0], utils.converter_currency_cny_usd(prices[0]))

        except:
            await bot.send_message(
                pretty.goods, 
                "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                reply_markup = kb.good_kb(),
                parse_mode=types.ParseMode.MARKDOWN)
            
        b = config.template_2.format(
            link,
            counts,
            pokypki,
            m, avg[0], mx,
            utils.converter_currency_usd_rub(m), utils.converter_currency_usd_rub(avg[0]), utils.converter_currency_usd_rub(mx),
            now,
            utils.converter_currency_usd_rub(now),
            ab_all,
            utils.generator_autobuy(autobuy_dollars),
            utils.generator_autobuy_rub(autobuy_dollars),
        )
    if len(market_data) == 0:
        b = config.template_3
        profit = "⛔️ "
    try:
        steams_orders = parser.steam_parser(name)
    except:
            await bot.send_message(
                pretty.goods, 
                "НАС ТРАХНУЛ СТИМ. ладно... согласен, по пидорски поступил.",
                reply_markup = kb.good_kb(),
                parse_mode=types.ParseMode.MARKDOWN)
    try:
        rubles = utils.generator_steam(steams_orders[1])
        dollars = utils.generator_steam(steams_orders[0])
    except:
            await bot.send_message(
                pretty.goods, 
                "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                reply_markup = kb.good_kb(),
                parse_mode=types.ParseMode.MARKDOWN)
    try:
        marg = steam_margin(utils.converter_currency_cny_rub(prices[0]), steams_orders[1][0]['price'])
    except:
            await bot.send_message(
                pretty.goods, 
                "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                reply_markup = kb.good_kb(),
                parse_mode=types.ParseMode.MARKDOWN)
    print('near c template')
    c = config.template_4.format(
        f"https://steamcommunity.com/market/listings/252490/{urllib.parse.quote(name)}",
        dollars,
        rubles
    )
    a = config.template_1.format(
            name,
            data['icon_url'],
            profit,
            marg,
            buff_link,
            len(prices),
            "$, ".join(map(str, utils.converter_currency_cny_usd(prices))),
            "₽, ".join(map(str, utils.converter_currency_cny_rub(prices))),
            utils.generator_buys(buys),
            utils.generator_buys_rub(buys)
        )
    print('after a template near message')
    message_text = a + b + c
    await bot.send_message(
            pretty.goods, 
            message_text,
            reply_markup = kb.good_kb(),
            parse_mode=types.ParseMode.MARKDOWN)



async def worker_many(bot):
    all_items = parser.get_all_items()
    try:
        for item in all_items:

            data = parser.buff_rust_prices(item)
            buff_link = "https://buff.163.com/goods/{}?from=market#tab=selling".format(item)

            name = data['name']
            prices = data['prices']
            buys = parser.buff_buyers(item)
            message_text = ""
    
            market_data = parser.market_rust_all(data['name'])
            if len(market_data) != 0:
                link = market_data[0]['link']
                try:
                    extend = parser.market_rust_extended(link)
                except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ РАСТ.ТМ. ПИДАРАСЫ?",
                        parse_mode=types.ParseMode.MARKDOWN)
                    
                counts = len(market_data)
                pokypki = extend['buys']
                m = extend['min_price']
                avg = extend['averange'],
                mx = extend['max_price']
                now = extend['prices']
                ab_all = extend['autobuy']['all']
                autobuy_dollars = extend['autobuy']['requests']
                try:
                    profit = margin(now[0], utils.converter_currency_cny_usd(prices[0]))
                except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                        parse_mode=types.ParseMode.MARKDOWN)
                    
                b = config.template_2.format(
                    link,
                    counts,
                    pokypki,
                    m, avg[0], mx,
                    utils.converter_currency_usd_rub(m), utils.converter_currency_usd_rub(avg[0]), utils.converter_currency_usd_rub(mx),
                    now,
                    utils.converter_currency_usd_rub(now),
                    ab_all,
                    utils.generator_autobuy(autobuy_dollars),
                    utils.generator_autobuy_rub(autobuy_dollars),
                )
            if len(market_data) == 0:
                b = config.template_3
            try:
                steams_orders = parser.steam_parser(name)
            except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ СТИМ. ладно... согласен, по пидорски поступил.",
                        parse_mode=types.ParseMode.MARKDOWN)
            try:
                rubles = utils.generator_steam(steams_orders[1])
                dollars = utils.generator_steam(steams_orders[0])
            except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                        parse_mode=types.ParseMode.MARKDOWN)
            try:
                marg = steam_margin(utils.converter_currency_cny_rub(prices[0]), steams_orders[1][0]['price'])
            except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                        parse_mode=types.ParseMode.MARKDOWN)
            c = config.template_4.format(
                f"https://steamcommunity.com/market/listings/252490/{urllib.parse.quote(name)}",
                dollars,
                rubles
            )
            try:
                a = config.template_1.format(
                        name,
                        data['icon_url'],
                        profit,
                        marg,
                        buff_link,
                        len(prices),
                        "$, ".join(map(str, utils.converter_currency_cny_usd(prices))),
                        "₽, ".join(map(str, utils.converter_currency_cny_rub(prices))),
                        utils.generator_buys(buys),
                        utils.generator_buys_rub(buys)
                    )
            except:
                    await bot.send_message(
                        pretty.logs, 
                        "НАС ТРАХНУЛ КУРС ВАЛЮТ. ГНИДЫ.",
                        parse_mode=types.ParseMode.MARKDOWN)
            message_text = a + b + c
            await bot.send_message(
                    pretty.logs, 
                    message_text,
                    parse_mode=types.ParseMode.MARKDOWN)
    except:
        await bot.send_message(
                pretty.logs, 
                "НАС ТРАХНУЛ БОТ. ладно, бро, прости, зачилься реально как гнида поступил, извини брат",
                parse_mode=types.ParseMode.MARKDOWN)




