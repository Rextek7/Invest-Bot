# Импортируем необходимые библиотеки и модули
import os
import telebot
from dotenv import load_dotenv
from telebot import types
import Invest_bot
import requests
import shelve

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен доступа бота и токен доступа GIPHY из переменных окружения
TOKEN = os.getenv('TOKEN')
GIPH_TOKEN = 'c5AWpqgdxReyPCOw9p3QtU1JkBkaDLt9'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Создаем словарь для хранения данных о пользователе
user_data = {}

# Создаем базу данных для хранения id пользователей
db = shelve.open('users.db')

if 'users' not in db:
    db['users'] = set()

db.close()


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Отправляем сообщение с приветствием и инструкцией по использованию бота
    bot.send_message(message.chat.id, 'Приветствую! Данный бот позволит тебе освоиться в трейдинге. \n'
                                      'Он использует песочницу Тинькофф, чтобы ты научился торговать прежде чем '
                                      'выходить на настоящий рынок.\n'
                                      '\n'
                                      'Обрати внимание, что покупка и продажа '
                                      'акций возможна только во время работы биржи!\n'
                                      'То есть в рабочие дни с 10 до 18.45!\n'
                                      '\n'
                                      'Для начала тебе нужно создать собственную песочницу, либо же можешь '
                                      'использовать уже созданную:\n'
                                      'Для этого потребуется:\n'
                                      '1) Перейти на сайт: https://www.tinkoff.ru/invest/settings/api/ \n'
                                      '2) Выбрать: Создание токена для песочницы\n'
                                      '3) Нажать выпустить токен и скопировать его\n'
                                      '4) Открыть файл .env и вставить его в TOKEN_TIN=твой_токен\n'
                                      '\n'
                                      'Все доступные функции бота ты можешь узнать через команду /info. \n'
                                      'Чтобы использовать данные функции ты можешь использовать команду /help')
    # Добавляем нового пользователя в базу данных
    db_data = shelve.open('users.db')
    users = db_data['users']
    users.add(message.from_user.id)
    db_data['users'] = users
    db_data.close()


# Обработчик команды /info
@bot.message_handler(commands=['info'])
def info(message):
    # Отправляем сообщение с информацией о доступных командах бота
    inf = (" \n"
           "*На данный момент в боте доступны следующие команды:*\n"
           "\n"
           "*1) Создать новый счет:* \n"
           "Команда создает новый счет в песочнице\n"
           "*2) Получить список счетов:* \n"
           "Команда выводит все счета доступные на аккаунте\n"
           "*3) Рассылка данных о валютах:*\n"
           "Команда выводит актуальную информацию о Долларах, Юане и Золоте\n"
           "*4) Удалить счет:*\n"
           "Команда удаляет счет, *id которого ты введешь*\n"
           "*5) Пополнить счет:* \n"
           "Команда пополняет счет на n рублей и k копеек. *Потребуется id счета который необходимо пополнить*\n"
           "*6) Получить информацию о счете:* \n"
           "Команда выводит всю доступную информацию о счете. *Потребуется id счета*\n"
           "*7) Получить информацию о доступных акциях:* \n"
           "Команда выводит наименования акций, которыми ты можешь торговать\n"
           "*8) Получить информацию об акции:* \n"
           "Команда выводит информацию об акции. *Потребуется точное наименование акции*\n"
           "*9) Купить акции:* \n"
           "Команда позволяет купить виртуальную акцию. *Потребуется id счета и figi акции*\n"
           "*10) Продать акции:* \n"
           "Команда позволяет продать виртуальную акцию. *Потребуется id счета и figi акции*\n"
           "*11) Stonks:* \n"
           "Если stonks то stonks\n"
           "*12) No stonks:* \n"
           "F\n"
           )
    bot.send_message(message.chat.id, inf, parse_mode='Markdown')


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def bottons(message):
    # Создаем список списков кнопок
    buttons = [
        [
            types.InlineKeyboardButton(text='Создать новый счет', callback_data='create_new_account'),
            types.InlineKeyboardButton(text='Получить список счетов', callback_data='get_all_accounts')
        ],
        [
            types.InlineKeyboardButton(text='Рассылка данных о валютах', callback_data='get_currency_data'),
            types.InlineKeyboardButton(text='Удалить счет', callback_data='delete_account')
        ],
        [
            types.InlineKeyboardButton(text='Пополнить счет', callback_data='credit_account')
        ],
        [
            types.InlineKeyboardButton(text='Получить информацию о счете', callback_data='get_info_account'),
        ],
        [
            types.InlineKeyboardButton(text='Получить информацию о доступных акциях',
                                       callback_data='get_available_shares'),
        ],
        [
            types.InlineKeyboardButton(text='Получить информацию об акции', callback_data='get_share_data')
        ],
        [
            types.InlineKeyboardButton(text='Купить акцию', callback_data='buy_share'),
            types.InlineKeyboardButton(text='Продать акцию', callback_data='sell_share')
        ],
        [
            types.InlineKeyboardButton(text='Stonks', callback_data='send_stonks_gif'),
            types.InlineKeyboardButton(text='No stonks', callback_data='send_nostonks_gif')
        ]
    ]

    # Создаем объект InlineKeyboardMarkup и добавляем кнопки
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for row in buttons:
        keyboard.add(*row)

    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, 'Список доступных команд:', reply_markup=keyboard)


def send_message_to_all(message_text):
    # Получаем список id всех пользователей
    db_data = shelve.open('users.db')
    users = list(db_data['users'])
    db_data.close()
    # Отправляем всем пользователем телеграм-бота информацию о валютах
    for user_id in users:
        bot.send_message(user_id, message_text)


# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Если callback-запрос соответствует команде "create_new_account"
    if call.data == 'create_new_account':
        # Вызов функции из файла Invest_bot.py для создания нового счета
        accounts = Invest_bot.create_new_account()
        # Отправка результата работы функции пользователю
        bot.send_message(call.message.chat.id, accounts)
    # Если callback-запрос соответствует команде "get_all_accounts"
    elif call.data == 'get_all_accounts':
        # Вызов функции из файла Invest_bot.py для получения списка всех счетов
        accounts = Invest_bot.get_all_accounts()
        # Отправка результата работы функции пользователю
        bot.send_message(call.message.chat.id, accounts)
    # Если callback-запрос соответствует команде "get_currency_data"
    elif call.data == 'get_currency_data':
        # Вызов функции из файла Invest_bot.py для получения данных о валютах
        currency_data = Invest_bot.get_currency_data()
        # Отправка результата работы функции пользователям
        for data in currency_data:
            send_message_to_all(data)
    # Если callback-запрос соответствует команде "delete_account"
    elif call.data == 'delete_account':
        # Отправка сообщения пользователю с запросом account_id
        bot.send_message(call.message.chat.id, 'Введите account_id для удаления:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'delete_account', 'step': 1}
    # Если callback-запрос соответствует команде "get_info_account"
    elif call.data == 'get_info_account':
        # Отправка сообщения пользователю с запросом account_id
        bot.send_message(call.message.chat.id, 'Введите account_id для получения о нем информации:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'get_info_account', 'step': 1}
    # Если callback-запрос соответствует команде "credit_account"
    elif call.data == 'credit_account':
        # Отправка сообщения пользователю с запросом account_id
        bot.send_message(call.message.chat.id, 'Введите account_id для пополнения:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'credit_account', 'step': 1}
    # Если callback-запрос соответствует команде "get_share_data"
    elif call.data == 'get_share_data':
        # Отправка сообщения пользователю с запросом share_name
        bot.send_message(call.message.chat.id, 'Введите название акции для получения о ней информации:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'get_share_data', 'step': 1}
    # Если callback-запрос соответствует команде "buy_share"
    elif call.data == 'buy_share':
        # Отправка сообщения пользователю с запросом account_id
        bot.send_message(call.message.chat.id, 'Введите account_id для покупки:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'buy_share', 'step': 1}
    # Если callback-запрос соответствует команде "sell_share"
    elif call.data == 'sell_share':
        # Отправка сообщения пользователю с запросом account_id
        bot.send_message(call.message.chat.id, 'Введите account_id для продажи:')
        # Сохранение данных о пользователе
        user_data[call.message.chat.id] = {'command': 'sell_share', 'step': 1}
    # Если callback-запрос соответствует команде "get_available_shares"
    elif call.data == 'get_available_shares':
        # Вызов функции из файла Invest_bot.py для получения списка доступных акций
        inf = Invest_bot.get_available_shares()
        # Отправка результата работы функции пользователю
        bot.send_message(call.message.chat.id, inf)
    # Если callback-запрос соответствует команде "send_stonks_gif"
    elif call.data == 'send_stonks_gif':
        # Отправка гифки с тегом "stonks"
        url = f'https://api.giphy.com/v1/gifs/search?q=stonks&api_key={GIPH_TOKEN}'
        response = requests.get(url).json()
        gifs = response['data']
        gif = gifs[0]['images']['fixed_height']['url']
        bot.send_animation(call.message.chat.id, gif)
    # Если callback-запрос соответствует команде "send_nostonks_gif"
    elif call.data == 'send_nostonks_gif':
        # Отправка гифки с тегом "nostonks"
        gif_id = 'Oj8pUuT5FOpxHH9LIk'
        url = f'https://api.giphy.com/v1/gifs/{gif_id}?api_key={GIPH_TOKEN}'
        response = requests.get(url).json()
        gif = response['data']['images']['fixed_height']['url']
        bot.send_animation(call.message.chat.id, gif)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    user_id = message.chat.id

    # Если пользователь есть в словаре user_data
    if user_id in user_data:
        user_step = user_data[user_id]['step']

        # Если команда пользователя соответствует "delete_account"
        if user_data[user_id]['command'] == 'delete_account':
            if user_step == 1:
                # Получение account_id от пользователя
                account_id = message.text
                # Вызов функции из файла Invest_bot.py для удаления счета
                result = Invest_bot.delete_account(account_id)
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, 'Аккаунт успешно удален.')
                    # Удаление данных о пользователе
                    for key, value in user_data.items():
                        if 'command' in value and value['command'] == 'delete_account':
                            del user_data[key]
                            break
                else:
                    bot.send_message(message.chat.id, 'Ошибка при удалении аккаунта.')

        # Если команда пользователя соответствует "get_info_account"
        elif user_data[user_id]['command'] == 'get_info_account':
            if user_step == 1:
                # Получение account_id от пользователя
                account_id = message.text
                # Вызов функции из файла Invest_bot.py для получения информации о счете
                result = Invest_bot.get_info_account(account_id)
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, result)
                    # Удаление данных о пользователе
                    for key, value in user_data.items():
                        if 'command' in value and value['command'] == 'get_info_account':
                            del user_data[key]
                            break
                else:
                    bot.send_message(message.chat.id, 'Ошибка получения информации')

        # Если команда пользователя соответствует "get_share_data"
        elif user_data[user_id]['command'] == 'get_share_data':
            if user_step == 1:
                # Получение share_name от пользователя
                share_name = message.text
                # Вызов функции из файла Invest_bot.py для получения информации об акции
                result = Invest_bot.get_share_data(str(share_name))
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, result)
                    # Удаление данных о пользователе
                    for key, value in user_data.items():
                        if 'command' in value and value['command'] == 'get_share_data':
                            del user_data[key]
                            break
                else:
                    bot.send_message(message.chat.id, 'Ошибка получения информации')

        # Если команда пользователя соответствует "credit_account"
        elif user_data[user_id]['command'] == 'credit_account':
            if user_step == 1:
                # Получение account_id от пользователя
                account_id = message.text
                # Отправка сообщения пользователю с запросом количества рублей
                bot.send_message(message.chat.id, 'Введите количество рублей для пополнения:')
                # Сохранение account_id и обновление шага
                user_data[user_id]['account_id'] = account_id
                user_data[user_id]['step'] = 2
            elif user_step == 2:
                # Получение количества рублей от пользователя
                units = int(message.text)
                # Отправка сообщения пользователю с запросом количества копеек
                bot.send_message(message.chat.id, 'Введите количество копеек для пополнения:')
                # Сохранение количества рублей и обновление шага
                user_data[user_id]['units'] = units
                user_data[user_id]['step'] = 3
            elif user_step == 3:
                # Получение количества копеек от пользователя
                nano = int(message.text)
                # Вызов функции из файла Invest_bot.py для пополнения счета
                result = Invest_bot.credit_account(user_data[user_id]['account_id'], user_data[user_id]['units'], nano)
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, result)
                else:
                    bot.send_message(message.chat.id, 'Ошибка при пополнении аккаунта.')
                # Удаление данных о пользователе
                del user_data[user_id]

        # Если команда пользователя соответствует "buy_share"
        elif user_data[user_id]['command'] == 'buy_share':
            if user_step == 1:
                # Получение account_id от пользователя
                account_id = message.text
                # Отправка сообщения пользователю с запросом figi
                bot.send_message(message.chat.id, 'Введите figi акции:')
                # Сохранение account_id и обновление шага
                user_data[user_id]['account_id'] = account_id
                user_data[user_id]['step'] = 2
            elif user_step == 2:
                # Получение figi от пользователя
                figi = message.text
                # Отправка сообщения пользователю с запросом количества акций
                bot.send_message(message.chat.id, 'Введите количество акций для покупки:')
                # Сохранение количества акций и обновление шага
                user_data[user_id]['figi'] = figi
                user_data[user_id]['step'] = 3
            elif user_step == 3:
                # Получение количества акций от пользователя
                quantity = int(message.text)
                # Вызов функции из файла Invest_bot.py для покупки акции
                result = Invest_bot.buy_share(user_data[user_id]['figi'], quantity,
                                              user_data[user_id]['account_id'])
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, result)
                else:
                    bot.send_message(message.chat.id, 'Ошибка при покупки акций.')
                # Удаление данных о пользователе
                del user_data[user_id]

        # Если команда пользователя соответствует "sell_share"
        elif user_data[user_id]['command'] == 'sell_share':
            if user_step == 1:
                # Получение account_id от пользователя
                account_id = message.text
                # Отправка сообщения пользователю с запросом figi
                bot.send_message(message.chat.id, 'Введите figi акции:')
                # Сохранение account_id и обновление шага
                user_data[user_id]['account_id'] = account_id
                user_data[user_id]['step'] = 2
            elif user_step == 2:
                # Получение figi от пользователя
                figi = message.text
                # Отправка сообщения пользователю с запросом количества акций
                bot.send_message(message.chat.id, 'Введите количество акций для продажи:')
                # Сохранение количества акций и обновление шага
                user_data[user_id]['figi'] = figi
                user_data[user_id]['step'] = 3
            elif user_step == 3:
                # Получение количества акций от пользователя
                quantity = int(message.text)
                # Вызов функции из файла Invest_bot.py для продажи акции
                result = Invest_bot.sell_share(user_data[user_id]['figi'], quantity,
                                               user_data[user_id]['account_id'])
                # Отправка сообщения пользователю
                if result:
                    bot.send_message(message.chat.id, result)
                else:
                    bot.send_message(message.chat.id, 'Ошибка при продаже акций.')
                # Удаление данных о пользователе
                del user_data[user_id]
        else:
            # Отправка сообщения пользователю
            bot.send_message(message.chat.id, message.text)
    else:
        # Отправка сообщения пользователю
        bot.send_message(message.chat.id, message.text)
