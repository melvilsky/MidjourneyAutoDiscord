from playwright.sync_api import sync_playwright
from config import MESSAGE_REPEAT_COUNT, HEADLESS_MODE
from PromtGeneration import process_and_format_line, remove_first_line
from time import sleep
import os
import random

def run_discord_bot():
    session_file = "session.json"
    target_channel_url = "https://discord.com/channels/1303467036176809995/1326909088172347474"

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
                page.press(message_box_selector, "Enter")
                print(f"Отправлено сообщение: {formatted_message}")

                # Генерация случайной задержки
                delay = random.randint(3000, 7000)
                page.wait_for_timeout(delay)

            # Удаляем строку только после завершения всех повторений
            remove_first_line()
        else:
            print("Файл пуст или произошла ошибка.")

        browser.close()


def get_max_allowed_number(message_repeat_count):
    """
    Возвращает максимальное число (от 1 до 10), которое можно вводить
    заданное количество раз message_repeat_count.

    :param message_repeat_count: Количество ввода строки
    :return: Максимальное допустимое число
    """

    # Определяем правила максимального количества повторений для каждого числа
    def repeats_for_number(number):
        if number == 1:
            return 10
        elif number == 2:
            return 5
        elif number == 3:
            return 3
        elif number in [4, 5]:
            return 2
        else:  # Для чисел 6–10
            return 1

    # Ищем максимальное число, которое удовлетворяет условию
    for number in range(10, 0, -1):  # Проверяем числа от 10 до 1
        if message_repeat_count <= repeats_for_number(number):
            return number

    return None  # Если ничего не найдено (на случай некорректного ввода)

def start_discord_bot(message_repeat_count):
    """
    Выполняет вызов run_discord_bot заданное количество раз
    с рандомной задержкой между вызовами.

    :param message_repeat_count: Количество повторений.
    """
    allowed_number = get_max_allowed_number(message_repeat_count)
    for i in range(allowed_number):
        run_discord_bot()
        # Генерация случайной задержки
        delay = random.randint(10, 16)   # Приведение к секундам
        print(f"Задержка перед следующим запуском: {delay} секунд")
        sleep(delay)

if __name__ == "__main__":
    while True:
        # Проверяем, есть ли строки в файле
        with open("mj_gen.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Если файл пуст, прерываем цикл
        if not lines:
            print("Промты закончились, файл mj_gen.txt пуст. Добавьте новые запросы и перезапустите скрипт.")
            break

        # Если файл не пуст, запускаем бот
        start_discord_bot(MESSAGE_REPEAT_COUNT)