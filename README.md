# OrderParser
Синхронизация с Google sheets, получение данных из таблицы и добавление в БД на PostgreSQL


## Установка и запуск:
## База данных:ф
### в консоли сервера:
sudo apt install postgresql postgresql-contrib -y #установит postgresql 
sudo -u postgres psql -c 'select now()' #проверит, что postgresql запущен и работает
sudo service postgresql restart # перезапустит, если установлен, но не работает
sudo -u postgres psql #запустит командную строку сервера postgresql
### \? # справка по командам консольного клиента psql
### \h # справка по доступным командам SQL
### \h <команда> # справка по конкретной команде
### \l # список баз данных
### \du # список пользователей
### \dt # список таблиц
### \q # выйти 
CREATE DATABASE some_db_name; # создаст БД <some_db_name>. название бд
CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres'; # создаст нового пользователя c <postgres> именем и <'postgres'> паролем
ALTER USER postgres WITH PASSWORD 'postgres'; # поменяет пароль, если требуется, для пользователя <postgres> на <'postgres'>
GRANT ALL PRIVILEGES ON DATABASE some_db_name TO postgres; # даст все права доступа к БД <some_db_name> пользователю <postgres>
\q # выйдет из консоли управления PostgreSQL

python3 manage.py makemigrations # также отдельно для каждой папки проекта, указанной в INSTALED_APPS, например, -//- some_folder для 'backend.some_folder'
python3 manage.py migrate # выполнит миграции

## Celery (регулярные задачи)
## В корневую папку добавить docker-compose.yml:
version: "3" 

  services:
    redis:
      image: redis
      ports:
        - "6379:6379"

# Запуск celery:
> docker-compose up -d --build
> 
> celery -A OrderParser beat 
> 
> celery -A OrderParser worker -l INFO --pool=solo 

## Запуск сервера
> python manage.py runserver 
> 

## В .env в корне проекта создать .env и добавить: 
DJANGO_SECRET=<секретный токен доступа к ресурсу>

DEBUG=False

GOOGLE_ACCESS_JSON=<.json словарь в одну строку или путь до .json файла: https://habr.com/ru/post/483302/> 

ORDERS_GOOGLE_SHEET=<id страницы для получения данных>

ALLOWED_HOSTS=<ip адрес или web-адрес сервера, где будет располагаться сайт>

DB_ENGINE=django.db.backends.postgresql_psycopg2

DB_NAME=<имя БД, которое необходимо было указать при создании>

DB_USER=<имя пользователя БД, которое необходимо было указать при создании>

DB_PASSWORD=<пароль пользователя БД, которое необходимо было указать при создании>

DB_HOST=localhost

DB_PORT=5432
