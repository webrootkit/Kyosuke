import requests
from bs4 import BeautifulSoup
import argparse
import json
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
import random
import string
from stem import Signal
from stem.control import Controller
import time

# Настройки Tor
TOR_PROXY = "socks5://127.0.0.1:9050"

# Фейковые данные для генерации
FAKE_NAMES = ["Иван Петров", "Алексей Смирнов", "Дарья Ковалёва"]
FAKE_EMAIL_DOMAINS = ["@mail.ru", "@gmail.com", "@yandex.ru"]

# ---[ Функции для даркнета ]---
def get_tor_session():
    session = requests.session()
    session.proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
    return session

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(5)

def parse_darknet_forum(query):
    try:
        session = get_tor_session()
        url = f"http://forumzombiewh6jtwx.onion/search?q={query}"  # Пример форума
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='post')[:5]  # Первые 5 результатов
        return [p.text.strip() for p in posts]
    except Exception as e:
        return [f"Ошибка: {str(e)}"]

# ---[ Функции для Telegram ]---
def check_telegram(username):
    try:
        with TelegramClient('anon', 12345, '0123456789abcdef0123456789abcdef') as client:
            user = client.get_entity(username)
            return {
                'id': user.id,
                'username': user.username,
                'name': user.first_name,
                'last_seen': user.status.was_online if user.status else "N/A"
            }
    except Exception as e:
        return {"error": str(e)}

# ---[ Генератор фейковых данных ]---
def generate_fake_identity():
    name = random.choice(FAKE_NAMES)
    email = name.lower().replace(" ", ".") + random.choice(FAKE_EMAIL_DOMAINS)
    phone = "+79" + "".join(random.choices(string.digits, k=9))
    return {"name": name, "email": email, "phone": phone}

# ---[ Основная логика ]---
def main():
    parser = argparse.ArgumentParser(description="Reaper-X: Dark OSINT Tool")
    parser.add_argument("--target", help="Email/Username/Phone")
    parser.add_argument("--darknet", help="Поиск в даркнете", action="store_true")
    parser.add_argument("--telegram", help="Проверить Telegram", action="store_true")
    parser.add_argument("--fake", help="Сгенерировать фейковые данные", action="store_true")
    args = parser.parse_args()

    result = {}

    if args.target:
        if args.darknet:
            renew_tor_ip()
            result["darknet"] = parse_darknet_forum(args.target)
        if args.telegram:
            result["telegram"] = check_telegram(args.target)

    if args.fake:
        result["fake_identity"] = generate_fake_identity()

    # Сохранение в JSON
    with open("result.json", "w") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Результаты сохранены в result.json")

if __name__ == "__main__":
    main()