import time
import utils
import ParserClass
import Logic
import asyncio

parser = ParserClass.HuinyaParser()


async def some_callback(args):
    await hook(args)

def threader(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(some_callback(args))
    loop.close()


async def hook(bot):
    itid = 1
    while True:
        print('start loop')
        item = parser.buff_first_item()
        print(item, itid)
        if item != itid:
            itid = item
            await Logic.worker_one(bot, item)
    