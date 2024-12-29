# Online platform for electronics

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/doc/)
[![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)](https://www.jetbrains.com/pycharm/documentation/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white&color=092E20&labelColor=gray)](https://www.djangoproject.com/start/)
[![Django REST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)

## Backend part of online platform for electronics retail chain with API and admin panel
Приложение реализует онлайн-платформу торговой сети по продаже электроники с API-интерфейсом и админ-панелью.

### Требования
- [Python](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/download/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/download/)

### Установка и запуск
1. Клонируйте репозиторий с помощью команды:
```
git clone https://github.com/ialar/Skypro_test_assignment.git
```
2. Перейдите в папку проекта:
```
cd Skypro_test_assignment
```
3. Установите необходимые зависимости, выполнив команду:
```
pip install -r requirements.txt
```
4. Воспользуйтесь шаблоном .env.sample для создания файла `.env`.
5. Создайте БД, примените миграции и загрузите необходимые данные с помощью фикстур (.\fixtures\):
```
psql -U postgres  
postgres=# CREATE DATABASE <db_name>;
CREATE DATABASE
postgres=# \q
```
```
python manage.py loaddata fixtures/<name>.json
```
6. Чтобы создать суперпользователя, выполните команду:
```
python manage.py csu
```
7. Локально запустите сервер:
```
python manage.py runserver
```

### Доступ и работа с приложением
- Документация: http://localhost:8000/redoc/
- Админка: http://localhost:8000/admin/