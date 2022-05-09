from email import header
from aiogram import bot, types
from bs4 import BeautifulSoup as bs
import requests, json
from datetime import datetime
import re
import urllib.parse
import pretty

api_currency = "https://api.exchangerate-api.com/v4/latest/USD"


buff_url = "https://buff.163.com/api/market/goods?game=rust&page_num={}&page_size=80"
buff_item_url = "https://buff.163.com/api/market/goods/sell_order?game=rust&goods_id={}&page_num=1&sort_by=price.asc&mode=&allow_tradable_cooldown=1"
buff_buyers_url = "https://buff.163.com/api/market/goods/bill_order?game=rust&goods_id={}"
tm_url = "https://rust.tm/?t=all&search={}&sd=desc"



buff_header = pretty.buff_header
tm_header = pretty.tm_header
steam_headers = pretty.steam_headers


class HuinyaParser:

    def __init__(self) -> None:
        self.s_buff = requests.Session()
        self.s_buff.headers.update(buff_header)

        self.s_tm = requests.Session()
        self.s_tm.headers.update(tm_header)

        self.s_steam = requests.Session()
        self.s_steam.headers.update(steam_headers)

    def buff_first_item(self):
        link = "https://buff.163.com/api/market/goods?game=rust&page_num=1&page_size=1"
        r = self.s_buff.get(link, headers=buff_header)
        item_id = json.loads(r.text)
        return int(item_id['data']['items'][0]["id"])

    def buff_rust_price_one(self):
        
        link = "https://buff.163.com/api/market/goods?game=rust&page_num=1&page_size=1"
        r = self.s_buff.get(link)
        item_id = json.loads(r.text)['data']['items'][0]["id"]
        r = self.s_buff.get(buff_item_url.format(item_id))
        data = json.loads(r.text)['data']
        return_data = {
            'prices': [],
            'item_id': item_id,
            'name': data['goods_infos'][str(item_id)]['market_hash_name'],
            "steam_price": data['goods_infos'][str(item_id)]['steam_price'],
            "icon_url": data['goods_infos'][str(item_id)]['icon_url']
        }
        for item in data['items']:
            return_data['prices'].append(float(item['price']))
        return return_data

    def get_pages(self):
        r = self.s_buff.get(buff_url.format(1))
        data = json.loads(r.text)['data']
        return int(data['total_page'])

    def buff_rust_prices(self, item_id):
        r = self.s_buff.get(buff_item_url.format(item_id))
        data = json.loads(r.text)['data']
        return_data = {
            'prices': [],
            'name': data['goods_infos'][str(item_id)]['market_hash_name'],
            "steam_price": data['goods_infos'][str(item_id)]['steam_price'],
            "icon_url": data['goods_infos'][str(item_id)]['icon_url']
        }
        # c = requests.get(api_currency)
        # currencies = json.loads(c.text)['rates']
        # factor = float(currencies['CNY'])
        # for item in data['items']:
        #     return_data['prices'].append(
        #         round(float(item['price']) / factor, 2)
        #     )
        for item in data['items']:
            return_data['prices'].append(float(item['price']))
        return return_data

    def buff_rust(self, page: int):
        return_data = []
        r = self.s_buff.get(buff_url.format(int(page)))
        data = json.loads(r.text)['data']
        items = data['items']
        for item in items:
            return_data.append(item['id'])
        return return_data

    def buff_buyers(self, good_id):
        r = self.s_buff.get(buff_buyers_url.format(good_id))
        data = json.loads(r.text)['data']
        items = data['items']
        return_data = []
        for item in items[:3]:
            price = item['price']
            time = item['buyer_pay_time']
            ts = int(time)
            return_data.append(
                {
                    'price': price,
                    'date': datetime.utcfromtimestamp(ts).strftime('%d.%m.%y')
                }
            )
        return return_data

    def market_rust_all(self, name):
        r = self.s_tm.get(tm_url.format(name))
        soup = bs(r.text, 'lxml')
        div = soup.find('div', {'class': 'market-items'})
        links = div.find_all('a')
        return_data = []
        for link in links:
            link_name = link.find('div', {'class': 'name'}).text.replace("\n", "").strip().lower()
            print(link_name)
            if link_name == name.lower():
                img = link.find('div', {'class': 'imageblock'})
                price = img.find('div', {'class': 'price'}).text
                data = {
                    "price": price.replace('\xa0', ''),
                    "link": "https://rust.tm{}".format(link['href'])
                }
                return_data.append(data)
        return return_data

    # def market_rust_all(self, name):
    #     r = self.s_tm.get(tm_url.format(name))
    #     soup = bs(r.text, 'lxml')
    #     div = soup.find('div', {'class': 'market-items'})
    #     links = div.find_all('a')
    #     return_data = []
    #     for link in links:
    #         img = link.find('div', {'class': 'imageblock'})
    #         price = img.find('div', {'class': 'price'}).text
    #         data = {
    #             "price": price.replace('\xa0', ''),
    #             "link": "https://rust.tm{}".format(link['href'])
    #         }
    #         return_data.append(data)
    #     return return_data

    def market_rust_extended(self, link):
        r = self.s_tm.get(link)
        soup = bs(r.text, 'lxml')
        return_data = {
            "buys": "",
            "min_price": "",
            "averange": "",
            "max_price": "",
            "prices": [],
            "autobuy": {
                'all': "",
                "requests": []
            }
        }
        prices = soup.find('div', {'class': 'ip-prices'})
        spans = prices.find_all('span')
        for span in spans[:-1]:
            if "предложение" in span.text or "предложения" in span.text or "предложений" in span.text:
                continue
            if "предложение" not in span.text or "предложения" not in span.text or "предложений" not in span.text: 
                return_data['prices'].append(float(span.text.replace("\xa0", "")))
        item_stats = soup.find_all('div', {'class': 'rectanglestats'})
        autobuy = item_stats[1]
        zxc = autobuy.find_all('div', {'class': 'rectanglestat'})
        for ind, stat in enumerate(zxc):
            b = stat.find('b').text.replace("\xa0", "")
            div = stat.find('div').text
            if ind == len(zxc) - 1:
                break
            if ind == 0:
               return_data['autobuy']['all'] = b
            if div != None and div != "Всего запросов":
                return_data['autobuy']['requests'].append(
                    {
                        "request_price": float(b),
                        "request_count": div.split(" ")[0]
                    }
                )
        stats = item_stats[0]
        for ind, stat in enumerate(stats.find_all("div", {'class': 'rectanglestat'})):
            t = stat.find('b').text.replace("\xa0", "")
            if ind == 0:
                return_data['buys'] = t
            if ind == 1:
                a = float(t)
                return_data['min_price'] = round(float(t), 2)
            if ind == 2:
                return_data['averange'] = round(float(t), 2)
            if ind == 3:
               return_data['max_price'] = round(float(t), 2)
        return return_data


    def steam_parser(self, name):
        r = self.s_steam.get("https://steamcommunity.com/market/listings/252490/{}".format(urllib.parse.quote(name)))
        result = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(r.text))
        name_id = result[0]
        r = self.s_steam.get(
            f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=1&item_nameid={name_id}&two_factor=0"
        )
        orders = json.loads(r.text)['sell_order_graph']
        dollar_orders = []
        for order in orders[:3]:
            dollar_orders.append(
                {
                    'price': float(order[0]),
                    'counts': float(order[1])
                }
            )
        r = self.s_steam.get(
            f"https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid={name_id}&two_factor=0"
        )
        orders = json.loads(r.text)['sell_order_graph']
        rub_orders = []
        for order in orders[:3]:
            rub_orders.append(
                {
                    'price': float(order[0]),
                    'counts': float(order[1])
                }
            )
        return dollar_orders, rub_orders

    def get_all_items(self):
        pages = self.get_pages()
        print("[get_all_items] {} pages!".format(pages))
        all_items = []
        for page in range(1, 2): # FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            items = self.buff_rust(page)
            all_items += items
            print("[get_all_items] {} page.".format(page))
        return all_items


