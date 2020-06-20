# free-food 
## FreeFood - фудшеринг чат-бот 
Этот чат-бот создан, чтобы «спасать» пригодную для употребления пищу. Бот для социальной сети «ВКонтакте» помогает найти бесплатные продукты заданной пользователем категории или категорий и отправляет ему релевантные сообщения. Переходя по объявлениям прямо в сообщениях, человек сможет первым зарезервировать эти продукты для себя. Пользователь имеет возможность указывать конкретные сообщества и получать  актуальные записи в режиме реального времени.
Стек решений:
- vk_api
- Python
- SQLite
- pymorphy2
	
Уникальность: Возможность указания конкретных сообществ, рассылка актуальных объявлений в режиме реального времени, приятный интерфейс.

## Инструкция
- [ ] Переходите по ссылке к чат боту [FreeFood](https://vk.com/freefood_app), авторизируйтесь в вконтакте и перейдите в диалог с ботом
- [ ] Введите ваш город, который будет использоваться для фильтрации постов
- [ ] Введите ссылки на группу/группы по одной боту
- [ ] Выберите категории для поиска нужной вам информации и начните поиск
- [ ] Бот изначально пришлет все посты релевантные вам, дата опубликования которых меньбше одного дня и после этого будет уведомлять вас на наличие новых постов
- [ ] Вы можете ввести новые значения отказавшись от рассылки и получать информацию уже по другим критериям

## Используемые библиотеки в python 
- requests
- re
- sqlite3
- pymorphy3
- datetime
- os
- json
- vk_api
- random
- time
- 

## Основа кода
Основая часть проекта находится в файле main.py, где собираются все модули воедино, пишется основа бота и главный цикл

```python
# импорт библиотек
import vk_api
import os
import json
import random
import datetime
import sqlite3
from functions import func_db
from functions import parcing

admin = 'id_of_admin(type-int)' # id админа в ВК

# ---SETTINGS VK---#
token = "your_token"  # api-key
vk = vk_api.VkApi(token=token)
vk._auth_token()
# ---SETTINGS VK---#

# инициализация db.sqlite
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()


def get_button(label, color, payload=''):  # функция вызова клавиатуры
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

# keyboards_categories
keyboard_category_1 = {"one_time": False, "buttons": [
                                                    [
                                                    get_button(label="Фрукты", color="primary"), 
                                                    get_button(label="Овощи", color="primary")
                                                    ],
                                                    [
                                                    get_button(label="Мясо", color="primary"), 
                                                    get_button(label="Еще (2 стр.)", color="negative")],
                                                    [
                                                    get_button(label="Принять", color="positive")]
                                                    ]}
keyboard_category_1 = json.dumps(keyboard_category_1, ensure_ascii=False).encode('utf-8')
keyboard_category_1 = str(keyboard_category_1.decode('utf-8'))
keyboard_category_2 = {"one_time": False, "buttons": [
                                                    [
                                                    get_button(label="Сдобное", color="primary"), 
                                                    get_button(label="Напитки", color="primary")
                                                    ], 
                                                    [
                                                    get_button(label="Сладости", color="primary"), 
                                                    get_button(label="Назад (1 стр.)", color="negative")],
                                                    [
                                                    get_button(label="Принять", color="positive")]
                                                    ]}
keyboard_category_2 = json.dumps(keyboard_category_2, ensure_ascii=False).encode('utf-8')
keyboard_catgeory_2 = str(keyboard_category_2.decode('utf-8'))

#keyboards_groups
keyboard_group = {"one_time": False, "buttons": [
                                                [
                                                get_button(label="Принять", color="positive")
                                                ]
                                                ]}
keyboard_group = json.dumps(keyboard_group, ensure_ascii=False).encode('utf-8')
keyboard_group = str(keyboard_group.decode('utf-8'))

#keyboard_in
keyboard_in = {"one_time": False, "buttons": [
                                            [
                                            get_button(label="Остановить поиск", color="negative")
                                            ],                                               
                                            ]}
keyboard_in = json.dumps(keyboard_in, ensure_ascii=False).encode('utf-8')
keyboard_in = str(keyboard_in.decode('utf-8'))


def start_register(id):  # функция проверки и регистрации пользователя в БД
    users_temp = func_db.select_all_id()
    users = []
    for user in users_temp:
        users.append(user[0])
    if id not in users:  # если юзера нет в БД, то регаем его
        func_db.insert_user(id, "", "", 0)


def accept_groups(id): # функция подтверждения введенных сообществ
    groups = func_db.select_groups(id)[0][0]
    if len(groups) == 0:
        return vk.method("messages.send", {"peer_id": id, "message": "Укажите, пожалуйста, хотя бы одну ссылку на сообщество в поле ввода сообщений.", "random_id": random.randint(1, 2147483647)})
    info = "Были выбраны следующие сообщества: " + groups[0:-1].replace(",", ", ")
    vk.method("messages.send", {"peer_id": id, "message": info, "random_id": random.randint(1, 2147483647)})
    func_db.edit_status(id, 1)
    category_info = "Пришло время выбрать категории еды для того, чтобы мы знали, какие объявления вам предлагать!\nПожалуйста, выберите нужные вам категории на клавиатуре:"
    vk.method("messages.send", {"peer_id": id, "message": category_info, "keyboard": keyboard_category_1, "random_id": random.randint(1, 2147483647)})  


def finish_register(id): # функция завершения регистрации пользователя в БД
    categories = func_db.select_categories(id)
    info = "Были выбраны следующие категории: " + categories[0][0][0:-1].replace(",", ", ")
    vk.method("messages.send", {"peer_id": id, "message": info, "random_id": random.randint(1, 2147483647)})
    finish = "Анкета заполнена!"
    func_db.edit_status(id, 2)
    vk.method("messages.send", {"peer_id": id, "message": finish, "keyboard": keyboard_in,"random_id": random.randint(1, 2147483647)})


def send_food(users_list): # функция рассылки объявлений
    temp_time = datetime.datetime.now()
    static_time = datetime.datetime(temp_time.year, temp_time.month, temp_time.day, 0, 1)
    current_time = datetime.datetime.now()
    delta_time = str(current_time - static_time)[:5]
    for user in users_list:
        try:
            # [id, categories, groups, status]
            if user[3] == 2:
                for group in user[2].split(",")[0:-1]:
                    results = parcing._Food(parcing._Parcing(group[group.rfind("/")+1:len(group)], delta_time), user[1].split(",")[0:-1])
                    for category in results.keys():
                        for link in results[category]:
                            message = "В категории " + category + " было найдено объявление для Вас!\n" + link
                            vk.method("messages.send", {"peer_id": user[0], "message": message, "attachment": link[15:],"keyboard": keyboard_in,  "random_id": random.randint(1, 2147483647)})
        except Exception as ex:
            print(ex)         

# статусы
# 0 - юзер заполняет сообщества
# 1 - юзер выбирает категории
# 2 - юзер готов к рассылке

# ---ОСНОВНОЙ ЦИКЛ---#
while True:
    next_time = [int(datetime.datetime.now().strftime('%H')), int(datetime.datetime.now().strftime('%M'))]
    next_time = next_time[0]*60+next_time[1]
    try:	
        while True:
            try:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    user_word = messages["items"][0]["last_message"]["text"]
                    start_register(id)
                    if func_db.select_status(id)[0][0] == 0:  # если пользователь не зарегистрирован
                        group_info = "Когда Вы добавите все необходимые ссылки, то нажмите на кнопку \"Принять\"."
                        if user_word == "Начать":
                            vk_info = vk.method("users.get", {"user_ids": int(id)})
                            name = vk_info[0].get('first_name')
                            info = name + ", добро пожаловать в FreeFood!\nДля работы бота необходимо дать ссылки на сообщества, в которых будет производиться поиск еды.\nКопируйте и вставляйте адреса сообществ по одному прямо в поле сообщений."
                            vk.method("messages.send", {"peer_id": id, "message": info, "keyboard": keyboard_group, "random_id": random.randint(1, 2147483647)})
                        elif user_word == "Принять":
                            accept_groups(id)
                        else:
                            func_db.edit_group(id, user_word)
                            vk.method("messages.send", {"peer_id": id, "message": group_info, "keyboard": keyboard_group, "random_id": random.randint(1, 2147483647)})
                    elif func_db.select_status(id)[0][0] == 1: # если пользователь не выбрал категории
                        category_info = "Пожалуйста, выберите нужные вам категории:"
                        if user_word == "Еще (2 стр.)":
                            vk.method("messages.send", {"peer_id": id, "message": category_info, "keyboard": keyboard_category_2, "random_id": random.randint(1, 2147483647)})                 
                        elif user_word == "Назад (1 стр.)":
                            vk.method("messages.send", {"peer_id": id, "message": category_info, "keyboard": keyboard_category_1, "random_id": random.randint(1, 2147483647)})
                        elif user_word == "Фрукты" or user_word == "Овощи" or user_word == "Мясо" or user_word == "Сдобное" or user_word == "Напитки" or user_word == "Сладости":
                            func_db.edit_category(id, user_word)
                            info = "Категория " + user_word + " добавлена!"
                            vk.method("messages.send", {"peer_id": id, "message": info, "keyboard": keyboard_category_1, "random_id": random.randint(1, 2147483647)})
                        elif user_word == "Принять":
                            finish_register(id)
                        else:
                            vk.method("messages.send", {"peer_id": id, "message": "Пожалуйста, выберите ниже представленные категории:", "keyboard": keyboard_category_1, "random_id": random.randint(1, 2147483647)})
                    elif func_db.select_status(id)[0][0] == 2:  # пользователь в поиске объявлений
                        if user_word == "Остановить поиск":
                            func_db.del_user(id)
                            info = "Поиск продуктов остановлен.\n\nДля работы бота необходимо дать ссылки на сообщества, в которых будет производиться поиск еды.\nКопируйте и вставляйте адреса сообществ по одному прямо в поле сообщений."
                            vk.method("messages.send", {"peer_id": id, "message": info, "keyboard": keyboard_group, "random_id": random.randint(1, 2147483647)})
                        else:
                            vk.method("messages.send", {"peer_id": id, "message": "Поиск продуктов...","keyboard": keyboard_in,  "random_id": random.randint(1, 2147483647)})
                now_time = [int(datetime.datetime.now().strftime('%H')), int(datetime.datetime.now().strftime('%M'))]
                now_time = now_time[0]*60+now_time[1]
                if now_time > next_time:
                    next_time += 1  # задержка парсинга в минутах
                    send_food(func_db.select_all_users())
            except Exception as ex:
                print(ex)
                vk.method("messages.send", {"peer_id": admin, "message": str(ex),"keyboard": keyboard_category_1,  "random_id": random.randint(1, 2147483647)})
    except Exception as ex:
        print(ex)
        continue
# ---ОСНОВНОЙ ЦИКЛ---#

```
