# from bs4 import BeautifulSoup as bs
# import requests, json, urllib.parse


# headers = {
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
# }
# s = requests.Session()
# s.headers.update(headers)
# print("=> Session started.")

# def margin(tm, buff):
#     return ((tm - buff) / tm) * 100

# def get_tm_price(name, s):
#     url = "https://market.csgo.com/?t=all&search={}&sd=desc"
#     encode_name = urllib.parse.quote(name)

#     r = s.get(url.format(encode_name))
#     soup = bs(r.text, 'lxml')
#     div = soup.find('div', {'class': 'market-items'})
#     links = div.find_all('a')
#     for link in links:
#         img = link.find('div', {'class': 'imageblock'})
#         price = img.find('div', {'class': 'price'}).text
#         print("{}; https://market.csgo.com{}".format(price, link['href']))


# def get_rust_items():
#     return_data = []
#     r = s.get("https://buff.163.com/api/market/goods/buying?game=rust&page_num=1&_=1650927141410")
#     data = json.loads(r.text)['data']
#     items = data['items']
#     for item in items:
#         item_id = item['id']
#         max_price = item['buy_max_price']
#         buy_num = item['buy_num']
#         name = item['name']
#         quick_price = item['quick_price']
#         steam = item['steam_market_url']
#         data = {
#             'name': name,
#             'steam_link': steam,
#             'buy_num': buy_num,
#             'max_price': max_price
#         }
#         return_data.append(data)
#     return return_data

# def get_buff_items():
#     r = s.get("https://buff.163.com/api/market/goods/buying?game=csgo&page_num=1&_=1650585562545")
#     data = json.loads(r.text)['data']
#     # page_now = data['page_num']
#     # page_max = data['total_page']
    
#     items = data['items']
#     for item in items:
#         item_id = item['id']
#         max_price = item['buy_max_price']
#         buy_num = item['buy_num']
#         name = item['name']
#         quick_price = item['quick_price']
#         steam = item['steam_market_url']
#         t = (item_id, name, buy_num, quick_price, max_price, steam)
#         print("{:<8} {:<10} {:<10} {:<10} {:<10} {:<10}".format(item_id, name, buy_num, quick_price, max_price, steam))



# def get_tm_rust_price(name):
#     url = "https://rust.tm/?t=all&search={}&sd=desc".format(name)
#     encode_name = urllib.parse.quote(name)

#     r = s.get(url.format(encode_name))
#     soup = bs(r.text, 'lxml')
#     div = soup.find('div', {'class': 'market-items'})
#     links = div.find_all('a')
#     return_data = []
#     for link in links:
#         img = link.find('div', {'class': 'imageblock'})
#         price = img.find('div', {'class': 'price'}).text
#         data = {
#             "price": price,
#             "link": link['href']
#         }
#         return_data.append(data)
#     return return_data
        

import requests, json

api_currency_usd = "https://api.exchangerate-api.com/v4/latest/usd"

api_currency_cny = "https://api.exchangerate-api.com/v4/latest/cny"

s = requests.Session()


def converter_currency_cny_usd(prices):
    c = json.loads(s.get(api_currency_cny).text)['rates']['USD']
    if type(prices) == list: 
        pr = []
        for price in prices:
            pr.append(
                round(price * float(c), 2)
            )
        return pr
    if type(prices) == float:
        return round(prices * float(c), 2)

def converter_currency_cny_rub(prices):
    c = json.loads(s.get(api_currency_cny).text)['rates']['RUB']
    if type(prices) == list: 
        pr = []
        for price in prices:
            pr.append(
                round(price * float(c), 2)
            )
        return pr
    if type(prices) == float or type(prices) == int:
        return round(prices * float(c), 2)



def converter_currency_usd_rub(prices):
    c = json.loads(s.get(api_currency_usd).text)['rates']['RUB']
    if type(prices) == list: 
        pr = []
        for price in prices:
            pr.append(
                round(price * float(c), 2)
            )
        return pr
    if type(prices) == float:
        return round(prices * float(c), 2)


def generator_steam(data: list):
    p = ""
    for i in data:
        p += "{} ({}), ".format(i['price'], i['counts'])
    return p

def generator_buys(data: list):
    c = json.loads(s.get(api_currency_cny).text)['rates']['USD']
    p = ""
    for buy in data:
        p += "[{}$](http://{}.huinya.date), ".format(round(float(buy['price']) * float(c), 2), buy['date'])
    return p

def generator_buys_rub(data: list):
    c = json.loads(s.get(api_currency_cny).text)['rates']['RUB']
    p = ""
    for buy in data:
        p += "[{}₽](http://{}.huinya.date), ".format(round(float(buy['price']) * float(c), 2), buy['date'])
    return p 
# generator_buys_rub(["12"])