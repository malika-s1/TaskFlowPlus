# test_database.py
import os
import django
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlowPlus.settings')
django.setup()

# Проверяем соединение с базой
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print(" База данных подключена успешно")
except Exception as e:
    print(f" Ошибка подключения к базе: {e}")

# Проверяем существование таблиц
from django.db import connection
tables = connection.introspection.table_names()
print(f" Таблицы в базе: {tables}")

# Проверяем миграции
from django.db.migrations.executor import MigrationExecutor
executor = MigrationExecutor(connection)
print(f" Примененные миграции: {executor.loader.applied_migrations}")
