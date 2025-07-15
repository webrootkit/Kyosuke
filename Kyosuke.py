import requests
from bs4 import BeautifulSoup
import argparse
import json
from telethon.sync import TelegramClient
import random
import string
from stem import Signal
from stem.control import Controller
import time
import threading
import sys
from datetime import datetime

# Настройки
TOR_PROXY = "socks5://127.0.0.1:9050"
FAKE_NAMES = ["Иван Петров", "Алексей Смирнов", "Дарья Ковалёва"]
FAKE_EMAIL_DOMAINS = ["@mail.ru", "@gmail.com", "@yandex.ru"]

# ---[ Главное меню ]---
def show_banner():
    print(r"""
  _  __ _   _  ___  ___ _  __ ___ 
 | |/ /| | | |/ _ \/ __| |/ /| __|
 | ' < | |_| | (_) \__ \ ' < | _| 
 |_|\_\ \__,_|\___/|___/_|\_\|___|
           by webrootkit | 2024
    """)

def show_menu():
    print("\n[01] Поиск в даркнет-форумах (Tor)")
    print("[02] Проверка Telegram-аккаунтов")
    print("[03] Генератор фейковых данных")
    print("[04] Поиск по email в утечках")
    print("[05] Поиск по IP (Shodan)")
    print("[06] DOS-тестер (LOIC-style)")
    print("[07] Выход\n")

# ---[ Функции поиска ]---
def darknet_search(query):
    try:
        session = requests.session()
        session.proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        url = f"http://forumzombiewh6jtwx.onion/search?q={query}"
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [p.text.strip() for p in soup.find_all('div', class_='post')[:3]]
    except Exception as e:
        return [f"Ошибка: {str(e)}"]

def telegram_search(username):
    try:
        with TelegramClient('anon', 12345, '0123456789abcdef') as client:
            user = client.get_entity(username)
            return {
                'id': user.id,
                'username': user.username,
                'phone': user.phone,
                'last_seen': str(user.status.was_online)
            }
    except Exception as e:
        return {"error": str(e)}

def generate_fake_data():
    name = random.choice(FAKE_NAMES)
    email = name.lower().replace(" ", ".") + random.choice(FAKE_EMAIL_DOMAINS)
    return {
        "name": name,
        "email": email,
        "phone": f"+79{''.join(random.choices(string.digits, k=9))}",
        "address": f"ул. {random.choice(['Ленина', 'Гагарина'])} {random.randint(1, 100)}"
    }

# ---[ Основной цикл ]---
def main():
    show_banner()
    while True:
        show_menu()
        choice = input("[?] Введите команду: ").strip()

        if choice == "01":
            target = input("[+] Введите запрос для даркнета: ")
            results = darknet_search(target)
            print(f"\n[+] Результаты:\n{json.dumps(results, indent=2, ensure_ascii=False)}")

        elif choice == "02":
            username = input("[+] Введите Telegram @username: ")
            print(f"\n[+] Данные: {json.dumps(telegram_search(username), indent=2)}")

        elif choice == "03":
            count = int(input("[+] Сколько фейков сгенерировать? "))
            fakes = [generate_fake_data() for _ in range(count)]
            with open("fakes.json", "w") as f:
                json.dump(fakes, f, indent=2, ensure_ascii=False)
            print(f"\n[+] Сохранено в fakes.json")

        elif choice == "07":
            print("\n[!] Выход...")
            break

        else:
            print("\n[!] Неверная команда!")

if __name__ == "__main__":
    main()
