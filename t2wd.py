import requests
from colorama import init, Fore
import time
import os

# Инициализация colorama
init()

# Запрос данных от пользователя
trafficType = input("Введите тип трафика (data, voice или sms): ")
volume = input("Введите кол-во ГБ/минут/SMS: ")
cost = input("Введите цену лота: ")
limit = input("Введите кол-во отображаемых продавцов: ")
 
while True:
    # Формирование ссылки
    url = f"https://tele2.ru/api/exchange/lots?trafficType={trafficType}&volume={volume}&cost={cost}&offset=0&limit={limit}"
   
    # Задержка на 5 секунд
    time.sleep(5)
   
    # Отправка GET-запроса и получение данных с использованием headers
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Очистка экрана
    os.system('cls' if os.name == 'nt' else 'clear')

    # Сбор информации о лоте
    if trafficType == "data":
        trafficType = Fore.GREEN + " ГБ"
    elif trafficType == "voice":
        trafficType = Fore.GREEN + " минут(ы)"
    else:
        trafficType = Fore.GREEN + " SMS"
        
    print(Fore.GREEN + "Информация о лоте:")
    print(Fore.GREEN + "Лот:", volume + trafficType)
    print(Fore.GREEN + "Цена:", cost + " ₽")
    print("----------")
    
    # Извлечение необходимых полей из данных
    if "data" in data:
        for item in data["data"]:
            seller = item.get("seller", {})
            name = seller.get("name")
            emojis = seller.get("emojis")
            trafficType = item.get("trafficType")
            value = item.get("volume", {}).get("value")
            amount = item.get("cost", {}).get("amount")
            my = item.get("my")

            # Подкрашивание строки в зеленый, если продавец - не бот, и в красный - если бот.
            nameoutput = "Имя:"
            botoutput = "Бот:"
            emojioutput = "Эмодзи:"
            delimmer = "|"
            if name is None:
                name = "Загрузка имени..."
            if my is False:
                my = Fore.GREEN + str(my)
                name = Fore.GREEN + str(name)
                emojis = Fore.GREEN + str(emojis) + Fore.RESET
                emojioutput = Fore.GREEN + str(emojioutput)
                botoutput = Fore.GREEN + str(botoutput)
                nameoutput = Fore.GREEN + str(nameoutput)
            else:
                my = Fore.RED + str(my)
                name = Fore.RED + str(name)
                emojis = Fore.RED + str(emojis) + Fore.RESET
                emojioutput = Fore.RED + str(emojioutput)
                botoutput = Fore.RED + str(botoutput)
                nameoutput = Fore.RED + str(nameoutput)
         
            # Вывод информации на экран
            print(nameoutput, name, delimmer, botoutput, my, delimmer, emojioutput, emojis)
            print("----------")
