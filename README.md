# MidjourneyAutoDiscord
# Инструкция по настройке и запуску скрипта автоматического промтинга в Discord

## 1. Скачивание и распаковка архива
1. **Скачайте архив с проектом.**
2. **Разархивируйте его** в удобное для вас место на компьютере.
3. **Откройте папку проекта** через вашу среду разработки (например, VS Code, PyCharm или другой редактор).

## 2. Установка зависимостей
1. Откройте терминал (встроенный в вашу среду разработки или отдельно).
2. Убедитесь, что вы находитесь в папке проекта.
3. Выполните команду для установки всех необходимых библиотек:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Установка браузеров для Playwright
1. Убедитесь, что библиотека Playwright была установлена из `requirements.txt`. Если нет, выполните команду:
   ```bash
   pip install playwright
   ```
2. Установите браузеры для Playwright:
   ```bash
   playwright install
   ```
3. Для Linux-систем установите дополнительные зависимости:
   ```bash
   playwright install-deps
   ```
4. Проверьте корректность установки:
   ```bash
   playwright check
   ```

## 4. Настройка логина и пароля
1. Откройте файл `loginDate.py`. (Уже не актуально пропускаем этот шаг и переходим к следующему)
2. Пропишите свои данные:
   ```python
   login = "ваш_логин"
   password = "ваш_пароль"
   ```
3. Сохраните изменения.

## 5. Добавление промтов
1. Откройте файл `mj_gen.txt`.
2. Запишите промты построчно, например:
   ```
   Нарисуй красный дракон, летящий над горами.
   Сцена заката с силуэтом дерева.
   Снежная пустыня и белый медведь.
   ```

## 6. Последовательность запуска
1. **Запустите скрипт для авторизации в Discord:**
   ```bash
   python discord_login.py
   ```
   Убедитесь, что авторизация проходит успешно.

2. **После успешной авторизации запустите скрипт для отправки промтов:**
   ```bash
   python discord_print.py
   ```
Скрипт начнет обрабатывать файл `mj_gen.txt` и отправлять промты в указанный канал Discord.

## 7. Веб-интерфейс
Для управления отправкой промтов можно воспользоваться простым веб-интерфейсом. Он позволяет запускать и останавливать процесс, просматривать логи, редактировать настройки `config.yaml` и файл `mj_gen.txt`. Настройки сохраняются автоматически, а изменения в `mj_gen.txt` нужно сохранять кнопкой **Save**.

Запустите его командой:
```bash
python web_interface.py
```
После запуска откройте [http://127.0.0.1:5000](http://127.0.0.1:5000) в браузере.

## 8. Проверка работы
1. Откройте Discord.
2. Проверьте, что промты из файла `mj_gen.txt` отправляются в нужный канал.
3. Следите за логами в терминале для проверки статуса выполнения или выявления ошибок.

## Примечания
- Убедитесь, что используете Python версии 3.9 или выше.
- Если возникают ошибки, проверьте, все ли библиотеки и зависимости установлены корректно.
- Для установки зависимостей вручную используйте файл `requirements.txt`.

Если что-либо остается непонятным или возникает ошибка, обращайтесь за помощью.

