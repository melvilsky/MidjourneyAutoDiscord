from playwright.sync_api import sync_playwright
from loginDate import DISCORD_EMAIL, DISCORD_PASSWORD  # Импорт данных авторизации
from config import HEADLESS_MODE
import json

def save_session(context, session_file="session.json"):
    # Сохранение состояния контекста (cookies и localStorage) в файл
    storage_state = context.storage_state()
    with open(session_file, "w") as file:
        file.write(json.dumps(storage_state))

def login_and_save_session():
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=HEADLESS_MODE)
        context = browser.new_context()
        page = context.new_page()

        # Переход на сайт Discord
        page.goto("https://discord.com/login")

        # Ввод данных для входа из config.py
        page.fill('input[name="email"]', DISCORD_EMAIL)
        page.fill('input[name="password"]', DISCORD_PASSWORD)
        page.click('button[type="submit"]')

        # Ожидание завершения входа
        page.wait_for_timeout(5000)  # Подождите 5 секунд или настройте по необходимости

        # Сохранение данных сеанса
        save_session(context)

        # Закрытие браузера
        browser.close()

if __name__ == "__main__":
    login_and_save_session()