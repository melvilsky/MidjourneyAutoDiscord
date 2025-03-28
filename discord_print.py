from playwright.sync_api import sync_playwright
from load_config import TXT_PATH, MESSAGE_REPEAT_COUNT, HEADLESS_MODE, TARGET_CHANNEL_URL, WAITING_TIME
from PromtGeneration import process_and_format_line, remove_first_line
from time import sleep
import os
import random

def run_discord_bot():
    session_file = "session.json"
    target_channel_url = TARGET_CHANNEL_URL

    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=HEADLESS_MODE)

        if os.path.exists(session_file):
            context = browser.new_context(storage_state=session_file)
        else:
            context = browser.new_context()

        page = context.new_page()
        page.goto(target_channel_url)

        message_box_selector = 'div[role="textbox"]'
        page.wait_for_selector(message_box_selector)

        # Получаем строку один раз для повторения
        formatted_message = process_and_format_line()

        # Проверка, удалось ли получить строку
        if formatted_message:
            for _ in range(MESSAGE_REPEAT_COUNT):
                # Ввод сообщения в поле

                page.fill(message_box_selector, formatted_message)
                page.wait_for_timeout(500)
                page.press(message_box_selector, "Enter")
                print(f"📩 {formatted_message}")

                # Генерация случайной задержки
                delay = random.randint(500, 2000)
                page.wait_for_timeout(delay)

            # Удаляем строку только после завершения всех повторений
            remove_first_line()
        else:
            print("Файл пуст или произошла ошибка.")

        browser.close()


if __name__ == "__main__":
    while True:
        # Проверяем, есть ли строки в файле
        with open(TXT_PATH, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Если файл пуст, прерываем цикл
        if not lines:
            print("🔄 Промты закончились! 📂 Файл mj_gen.txt пуст. ✍️ Добавьте новые запросы и перезапустите скрипт. 🚀")
            break

        # Если файл не пуст, запускаем бот
        try:
            run_discord_bot()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        delay = random.randint(*WAITING_TIME)  # Время задержки
        print(f"⏳ Задержка перед следующим запуском... 🔄: {delay} секунд")
        sleep(delay)
