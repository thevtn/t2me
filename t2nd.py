import requests
from colorama import init, Fore
import time
import os
from requests.exceptions import JSONDecodeError, ConnectionError

init()

trafficType = input("Введите цифру типа трафика (1-ГБ, 2-минуты или 3-SMS): ")
traffic_types = {"1": "data", "2": "voice", "3": "sms"}
trafficType = traffic_types.get(trafficType, trafficType)
headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}
cost_url = f"https://tele2.ru/api/exchange/lots/stats/volumes?trafficType={trafficType}"
try:
   response = requests.get(cost_url, headers=headers)
   data = response.json()
except (JSONDecodeError, ConnectionError):
        print(Fore.YELLOW + "Ошибка парсинга: вы использовали t2nd.py слишком долго. \n Tele2 посчитали вашу сессию подозрительной и временно заблокировали ваш IP. \n Совет: для продолжения мониторинга, включите VPN и используйте t2wd.py или t2nd.py \n Если вы использовали t2wd.py, а не t2nd.py, то просто перезапустите программу :}")
        raise SystemExit
def get_cost(volume):
    for item in data['data']:
        if item['volume'] == volume:
            cost = item['minCost']
            return cost
    return None
volume = int(input("Введите кол-во ГБ/минут/SMS: "))
cost = get_cost(volume)
limit = input("Введите кол-во отображаемых продавцов: ")
 
while True:

    url = f"https://tele2.ru/api/exchange/lots?trafficType={trafficType}&volume={volume}&cost={cost}&limit={limit}"
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}
    try:
       response = requests.get(url, headers=headers)
       dump = response.json()

    except (JSONDecodeError, ConnectionError):
        print(Fore.YELLOW + "Ошибка парсинга: вы использовали t2nd.py слишком долго. \n Tele2 посчитали вашу сессию подозрительной и временно заблокировали ваш IP. \n Совет: для продолжения мониторинга, включите VPN и используйте t2wd.py или t2nd.py \n Если вы использовали t2wd.py, а не t2nd.py, то просто перезапустите программу :}")
        raise SystemExit

    os.system('cls' if os.name == 'nt' else 'clear')

    trafficType = " ГБ" if trafficType == "data" else " минут(ы)" if trafficType == "voice" else " SMS"
        
    print(f"{Fore.GREEN}Информация о лоте:")
    print(f"{Fore.GREEN}Лот: {volume}{trafficType}")
    print(f"{Fore.GREEN}Цена: {str(cost).replace('.0', '')} ₽")
    print(f"{Fore.WHITE}================={Fore.RESET}")

    if "data" in dump:
        for item in dump["data"]:
            seller = item.get("seller", {})
            name = seller.get("name")
            emojis = seller.get("emojis")
            trafficType = item.get("trafficType")
            my = item.get("my")

            nameis = "Имя:"
            botis = "Бот:"
            emojiis = "Эмодзи:"
            delimmer = "|"
            if name is None:
            	name = "Анонимный продавец"
            if my is False:
                nameis = Fore.GREEN + str(nameis)
                emojis = Fore.GREEN + str(emojis) + Fore.RESET
            else:
                nameis = Fore.RED + str(nameis)
                emojis = Fore.RED + str(emojis) + Fore.RESET

            print(nameis, name, delimmer, botis, my, delimmer, emojiis, emojis)
