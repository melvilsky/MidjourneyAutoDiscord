from load_config import *


def process_and_format_line():
    """
    Читает первую строку из файла, форматирует её и возвращает отформатированную строку.
    Строка не удаляется сразу.
    """
    path = TXT_PATH  # Локальная переменная для пути к файлу

    # Читаем содержимое файла
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Проверяем, есть ли строки в файле
    if not lines:
        return None


    # Получаем и форматируем первую строку
    description = lines[0].strip()
    formatted_message = (
        f"/imagine prompt:{description} "
        f"--ar {ar_value} "
        f"--style {style_value} "
        f"--c {c_value} "
        f"--s {s_value} "
        f"--q {quality_value} "
        f"--weird {weird_value} "
        f"--v {v_value} "
        f"--no {negative_value} "
        f"{add_value}"
    )

    # Возвращаем отформатированную строку (не удаляем строку сразу)
    return formatted_message


def remove_first_line():
    """
    Удаляет первую строку из файла после использования.
    """
    path = TXT_PATH  # Локальная переменная для пути к файлу

    # Читаем содержимое файла
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Удаляем первую строку и записываем оставшиеся строки обратно в файл
    if lines:
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines[1:])

if __name__ == "__main__":
    print(process_and_format_line())
