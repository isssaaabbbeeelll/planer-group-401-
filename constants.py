DATABASE_PATH = 'tasks.db' #Имя файла базы данных Sqlite

CREATE_TABLE_TASKS = '''
CREATE TABLE IF NOT EXISTS tasks 
(id INTEGER PRIMARY KEY, 
subject TEXT, 
description TEXT,
 due_date DATETIME,
  importance INTEGER)''' #Запрос SQL. Создаёт таблицу с заданиями

ALLOWED_IMPORTANCE_VALUES = [1, 2, 3] #Допускаемые значения важности заданий

ADD_TASKS_TO_TABLE = '''INSERT INTO tasks 
(subject, description, due_date, importance)
VALUES (?,?,?,?)'''   #Запрос SQL. Сохраняет добавленные задания в базу данных

IMPORT_TASKS_FROM_TABLE ='''SELECT subject, description, due_date, importance FROM tasks''' #Запрос SQL. Отображает задания задания из базы данных

