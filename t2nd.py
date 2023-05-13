import requests
from colorama import init, Fore
import time
import os
from requests.exceptions import JSONDecodeError, ConnectionError

init()

trafficType = input("Введите тип трафика (data, voice или sms): ")
volume = input("Введите кол-во ГБ/минут/SMS: ")
cost = input("Введите цену лота: ")
limit = input("Введите кол-во отображаемых продавцов: ")
 
while True:

    url = f"https://tele2.ru/api/exchange/lots?trafficType={trafficType}&volume={volume}&cost={cost}&offset=0&limit={limit}"

    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}
    try:
       response = requests.get(url, headers=headers)
       data = response.json()

    except (JSONDecodeError, ConnectionError):
        print( Fore.YELLOW + "Ошибка парсинга: вы использовали t2nd.py слишком долго. \n Tele2 посчитали вашу сессию подозрительной и временно заблокировали ваш IP. \n Совет: для продолжения мониторинга, включите VPN и используйте t2wd.py \n Если вы использовали t2wd.py, а не t2nd.py, то просто перезапустите программу :}")
        raise SystemExit(1)

    os.system('cls' if os.name == 'nt' else 'clear')

    if trafficType == "data":
        trafficType = " ГБ"
    elif trafficType == "voice":
        trafficType = " минут(ы)"
    else:
        trafficType = " SMS"
        
    print(Fore.GREEN + "Информация о лоте:")
    print(Fore.GREEN + "Лот:", volume + trafficType)
    print(Fore.GREEN + "Цена:", cost + " ₽")
    print(Fore.WHITE + "----------" + Fore.RESET)

    if "data" in data:
        for item in data["data"]:
            seller = item.get("seller", {})
            name = seller.get("name")
            emojis = seller.get("emojis")
            trafficType = item.get("trafficType")
            value = item.get("volume", {}).get("value")
            amount = item.get("cost", {}).get("amount")
            my = item.get("my")

            nameis = "Имя:"
            botis = "Бот:"
            emojiis = "Эмодзи:"
            delimmer = "|"
            if name is None:
            	name = "Анонимный продавец"
            if my is False:
                my = Fore.GREEN + str(my)
                name = Fore.GREEN + str(name)
                emojis = Fore.GREEN + str(emojis) + Fore.RESET
                emojiis = Fore.GREEN + str(emojiis)
                botis = Fore.GREEN + str(botis)
                nameis = Fore.GREEN + str(nameis)
            else:
                my = Fore.RED + str(my)
                name = Fore.RED + str(name)
                emojis = Fore.RED + str(emojis) + Fore.RESET
                emojiis = Fore.RED + str(emojiis)
                botois = Fore.RED + str(botis)
                nameis = Fore.RED + str(nameis)

            print(nameis, name, delimmer, botis, my, delimmer, emojiis, emojis)
