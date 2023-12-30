# Система тестировония студентов для ПИМУ
На этом сервисе пользователи смогут проходить тесты по курсам и смотреть статистику.
# Запуск проекта в dev-режиме
- Клонируйте репозиторий
```bash
git@github.com:DenisLukianov21/Tarasov.git
```
- Создайте и активируейте виртуальное окружение (для UNIX)
```bash
python3 -m venv env && source env/bin/activate
```
- Установите необходимые библиотеки
```bash
pip install -r requirements.txt
```
-Выполните миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
-Создайте админа
```bash
python manage.py createsuperuser
```
-Запустите приложение
```bash
python manage.py runserver
```
# Автор
Денис Лукьянов, Петр Единорогов
2024 г.