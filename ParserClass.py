from aiogram import bot, types
from bs4 import BeautifulSoup as bs
import requests, json
from datetime import datetime
import re
import urllib.parse

api_currency = "https://api.exchangerate-api.com/v4/latest/USD"


buff_url = "https://buff.163.com/api/market/goods?game=rust&page_num={}&page_size=80"
buff_item_url = "https://buff.163.com/api/market/goods/sell_order?game=rust&goods_id={}&page_num=1&sort_by=price.asc&mode=&allow_tradable_cooldown=1"
buff_buyers_url = "https://buff.163.com/api/market/goods/bill_order?game=rust&goods_id={}"
tm_url = "https://rust.tm/?t=all&search={}&sd=desc"

buff_header = {
    "Cookie": "P_INFO=380-989838838|1650356312|1|netease_buff|00&99|null&null&null#UA&null#10#0|&0||380-989838838; Locale-Supported=en; NTES_YD_SESS=0JikbwZfwPpVs1zn7rv_.MXP33v5VNOH8SH2brLTn1rIxEsuyJbzrrNlltE6TwzbxCWdqfrQqrJM1zY9Mb8XPkyv1o3sCUiAaE0eqHuwahQ6dwB_FC1EZs.vi44ig2RR1VAkAWVd_5rJD2PereoqX2ki5XK5AFD48ndVCQWR.RRsdH997bHjqvNAkwZhoFa0DMdgyYWXUpvCAJmcSH06DWzY0Htz2zMgmrQfOXGSisUsk; S_INFO=1650356312|0|0&60##|380-989838838; to_steam_processing_click220419T14894701241=1; to_steam_processing_click220419T14890631261=1; to_steam_processing_click220425T15271183701=1; session=1-vXRVRNMhvDxhekr_qqGo8xB4sYtNFb9b4WcYzRl6haci2037842870; game=rust; _ga=GA1.2.1304958935.1650355722; _gid=GA1.2.130948595.1650355722; Device-Id=sYVN3zG6xYbcQcvJUKLQ; csrf_token=Ijg2Y2YyZDM5ZjQ2ZGJkZjE0ZWNhOTZmM2U1YTI0M2QzMDY0ZDQ5ZjQi.FUtLrw.JPnZU0-Z26eppry3LBMwCdWiQqY; _ntes_nnid=425e523b63db53f1eac30854b296bfa4,1651067757502; _ntes_nuid=425e523b63db53f1eac30854b296bfa4",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


tm_header = {
    "cookie": "PHPSESSID=tlfuh96cjh9mp5r1rg5qhhatve; _csrf=NRA6KZ3zz2hyLdbdQaZQMSmyStb95p7N; goon=0; d2mid=ZPH9X7oQIpuM5VE2EnR5bb1ZTRf1Vq; d2netAuthStatus=checked",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

steam_headers = {
            "Cookie": "timezoneOffset=10800,0; _ga=GA1.2.1303873552.1649809671; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A1%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D; steamMachineAuth76561199114300721=2F539F3C71C4C35EDE73F1506255D9ED75CF481E; browserid=2537224299487212475; steamMachineAuth76561198127512332=EB471D0470DB7C66771C2E3ED9DD8746A597C348; steamMachineAuth76561198318380866=21D2D97F8238BB1D1A03213D991CDF9E92F6A312; steamRememberLogin=76561198318380866%7C%7C8c10418101b67478e92a16116efd8c39; strInventoryLastContext=440_2; recentlyVisitedAppHubs=1222670%2C4000; _gid=GA1.2.77098118.1651354887; sessionid=627ec16bd36776425493cec0; steamLoginSecure=76561198318380866%7C%7CF2B481BF4D1B2CC6BF4DD7D9878A07BA60F22FF8; webTradeEligibility=%7B%22allowed%22%3A0%2C%22reason%22%3A16416%2C%22allowed_at_time%22%3A1652042694%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1651437894%7D; steamCountry=UA%7Cea023a65bfc3d3aed40d6b0af8681474"
        }


class HuinyaParser:

    def __init__(self) -> None:
        self.s_buff = requests.Session()
        self.s_buff.headers.update(buff_header)

        self.s_tm = requests.Session()
        self.s_tm.headers.update(tm_header)

        self.s_steam = requests.Session()
        self.s_steam.headers.update(steam_headers)
                
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
            img = link.find('div', {'class': 'imageblock'})
            price = img.find('div', {'class': 'price'}).text
            data = {
                "price": price.replace('\xa0', ''),
                "link": "https://rust.tm{}".format(link['href'])
            }
            return_data.append(data)
        return return_data

    def market_rust_extended(self, link):
        r = self.s_tm.get(link)
        soup = bs(r.text, 'lxml')
        return_data = {
            "buys": "",
            "min_price": "",
            "averange": "",
            "max_price": "",
            "prices": []
        }
        prices = soup.find('div', {'class': 'ip-prices'})
        spans = prices.find_all('span')
        for span in spans[:-1]:
            if "предложение" in span.text or "предложения" in span.text or "предложений" in span.text:
                continue
            if "предложение" not in span.text or "предложения" not in span.text or "предложений" not in span.text: 
                return_data['prices'].append(float(span.text.replace("\xa0", "")))
        stats = soup.find("div", {'class': 'rectanglestats'})
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


