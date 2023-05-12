import requests
from colorama import init, Fore
import time
import os

init()

trafficType = input("Введите тип трафика (data, voice или sms): ")
volume = input("Введите кол-во ГБ/минут/SMS: ")
cost = input("Введите цену лота: ")
limit = input("Введите кол-во отображаемых продавцов: ")
 
while True:
 
    url = f"https://tele2.ru/api/exchange/lots?trafficType={trafficType}&volume={volume}&cost={cost}&offset=0&limit={limit}"
   
    time.sleep(5)
   
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}
    response = requests.get(url, headers=headers)
    data = response.json()

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
    print("----------")

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
