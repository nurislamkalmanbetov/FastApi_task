# FastAPI проект с PostgreSQL

Простое приложение на основе FastAPI для работы с пользователями, чатами и сообщениями, использующее PostgreSQL в качестве базы данных.

## Начало работы

### Установка зависимостей


pip install -r requirements.txt


### Запуск приложения 

uvicorn main:app --reload

### После выполнения этих команд, ваше приложение будет доступно по адресу: http://127.0.0.1:8000

### API Endpoints
### Пользователи
### Извлечение всех пользователей:

GET http://127.0.0.1:8000/users/

### Извлечение одного пользователя по имени

GET http://127.0.0.1:8000/user/?name=nuris

### Чаты
### Извлечение чатов пользователя:

GET http://127.0.0.1:8000/user_chats/6233e8cb-06bd-43b3-9e17-10ff9ed4c2a7/

### Сообщения
### Извлечение сообщений с возможностью фильтрации:

GET http://127.0.0.1:8000/messages/



1) Извлечение всех пользователей (нужны все поля) 
    - http://127.0.0.1:8000/users/  
2) Извлечение одного пользователя (нужны все поля) 
(Опционально) добавить параметр для фильтрации по id, username)
    - http://127.0.0.1:8000/user/?name=nuris
3) Извлечение чатов пользователя тех, в которых состоит пользователь, вместе с id и username пользователя, собеседника + фильтрация по полю status (нужны все поля) 
    - http://127.0.0.1:8000/user_chats/6233e8cb-06bd-43b3-9e17-10ff9ed4c2a7/
4) Извлечение сообщений с фильтрацией по sender_id, receiver_id, time_delivered (нужны все поля) 
    - http://127.0.0.1:8000/messages/ 