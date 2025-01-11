from config import ar_value, style_value, c_value, s_value, v_value, quality_value, weird_value

txt_path = "mj_gen.txt"  # Пример: замените на ваш путь

def process_and_format_line():
    """
    Читает первую строку из файла, форматирует её и возвращает отформатированную строку.
    Строка не удаляется сразу.
    """
    path = txt_path  # Локальная переменная для пути к файлу

    # Читаем содержимое файла
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Проверяем, есть ли строки в файле
    if not lines:
        print("Файл пуст.")
        return None

    # Получаем и форматируем первую строку
    description = lines[0].strip()
    formatted_message = f"/imagine prompt:{description} --ar {ar_value} --style {style_value} --c {c_value} --s {s_value} --q {quality_value} --weird {weird_value} --v {v_value}"

    # Возвращаем отформатированную строку (не удаляем строку сразу)
    return formatted_message


def remove_first_line():
    """
    Удаляет первую строку из файла после использования.
    """
    path = txt_path  # Локальная переменная для пути к файлу

    # Читаем содержимое файла
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Удаляем первую строку и записываем оставшиеся строки обратно в файл
    if lines:
        with open(path, 'w', encoding='utf-8') as file:
            file.writelines(lines[1:])