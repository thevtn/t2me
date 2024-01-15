import requests
from colorama import init, Fore
import time
import os
from requests.exceptions import JSONDecodeError, ConnectionError

init()

delay = input("Включить задержку? (Y/n): ").lower()
trafficType = input("Введите цифру типа трафика (1-ГБ или 2-минуты): ")
traffic_types = {"1": "data", "2": "voice", "3": "sms"}
trafficType = traffic_types.get(trafficType, trafficType)

volume = int(input("Введите кол-во ГБ/минут: "))
mincost = input("Минималка? (Y/n): ").lower()
yes = {'yes','y', 'ye', ''}
no = {'no','n'}
limit = input("Введите кол-во отображаемых продавцов: ")
def ErrorHandler():
    print(Fore.YELLOW + "Ошибка парсинга: потерян доступ к серверу.")
    raise SystemExit
if mincost in yes:
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}
    cost_url = f"https://tele2.ru/api/exchange/lots/stats/volumes?trafficType={trafficType}"
    try:
       response = requests.get(cost_url, headers=headers)
       data = response.json()
    except:
       ErrorHandler()
    def get_cost(volume):
        for item in data['data']:
            if item['volume'] == volume:
                cost = item["minCost"]
                return cost
        return None
    cost = get_cost(volume)
elif mincost in no:
    cost = input("Введите цену лота: ")
        
while True:
    url = f"https://tele2.ru/api/exchange/lots?trafficType={trafficType}&volume={volume}&cost={cost}&limit={limit}"
    headers = {"user-agent": "Mozilla/5.0 (Linux; Android 13; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"}

    try:
       if delay in yes:
          time.sleep(5)
       else:
          time.sleep(0)
       response = requests.get(url, headers=headers)
       dump = response.json()
    except:
       ErrorHandler()

    os.system('cls' if os.name == 'nt' else 'clear')
    
    trafficType = " ГБ" if trafficType == "data" else " минут(ы)" if trafficType == "voice" else " SMS"
     
    print(f"{Fore.GREEN}Информация о лоте:")
    print(f"{Fore.GREEN}Лот: {volume}{trafficType}")
    print(f"{Fore.GREEN}Цена: {str(cost).replace('.0', '')} ₽")
    print(f"{Fore.WHITE}{'-' * 35}{Fore.RESET}")
    print(f"{Fore.YELLOW}{'Имя':<20}{'Эмодзи'}{Fore.RESET}")
    print(f"{Fore.WHITE}{'-' * 35}{Fore.RESET}")
    if "data" in dump:
        try:
            for item in dump["data"]:
                seller = item.get("seller", {})
                name = seller.get("name")
                emojis = seller.get("emojis")
                trafficType = item.get("trafficType")
                my = item.get("my")

                name = "Анонимный продавец" if name is None else name
                if my is False:
                    name = Fore.GREEN + str(name)
                    emojis = Fore.GREEN + str(emojis) + Fore.RESET
                else:
                    name = Fore.RED + str(name)
                    emojis = Fore.RED + str(emojis) + Fore.RESET

                print(f"{Fore.WHITE}{name:<25}{emojis}{Fore.RESET}")
        except TypeError as e:
            os.system('clear')
            print(Fore.YELLOW + "Произошла ошибка при обработке данных.\nПожалуйста, проверьте правильность введенных данных и попробуйте снова.")
            raise SystemExit