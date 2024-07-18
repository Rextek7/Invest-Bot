# Импортируем функцию load_dotenv из модуля dotenv для загрузки переменных окружения из файла .env
from dotenv import load_dotenv
# Импортируем объект bot из модуля bot_base, который содержит основную логику работы бота
from bot_base import bot
# Загружаем переменные окружения из файла .env в текущее окружение
load_dotenv()

# Запускаем бота
if __name__ == '__main__':
    bot.polling(non_stop=True)
