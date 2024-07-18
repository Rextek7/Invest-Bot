# Импортируем необходимые модули и функции для работы с Тинькофф Инвестициями
import os
import uuid

from dotenv import load_dotenv
from tinkoff.invest import MoneyValue, OrderDirection, OrderType, exceptions
from tinkoff.invest.sandbox.client import SandboxClient

# Загружаем переменные окружения из файла .env в текущее окружение
load_dotenv()

# Получаем значение токена Тинькофф Инвестиций из переменных окружения
TOKEN_TIN = os.getenv('TOKEN_TIN')

# Создаем словарь с описанием статусов торговли
trading_status_map = {
    0: 'Торговый статус не определён',
    1: 'Недоступен для торгов',
    2: 'Период открытия торгов',
    3: 'Период закрытия торгов',
    4: 'Перерыв в торговле',
    5: 'Нормальная торговля',
    6: 'Аукцион закрытия',
    7: 'Аукцион крупных пакетов',
    8: 'Дискретный аукцион',
    9: 'Аукцион открытия',
    10: 'Период торгов по цене аукциона закрытия',
    11: 'Сессия назначена',
    12: 'Сессия закрыта',
    13: 'Сессия открыта',
    14: 'Доступна торговля в режиме внутренней ликвидности брокера',
    15: 'Перерыв торговли в режиме внутренней ликвидности брокера',
    16: 'Недоступна торговля в режиме внутренней ликвидности брокера'
}

EXECUTION_REPORT_STATUS = {
    0: 'none',
    1: 'Исполнена',
    2: 'Отклонена',
    3: 'Отменена пользователем',
    4: 'Новая',
    5: 'Частично исполнена'
}

ORDER_DIRECTION = {
    0: 'Значение не указано',
    1: 'Покупка',
    2: 'Продажа'
}


# Функция для создания нового счета в песочнице
def create_new_account():
    # Создаем объект клиента Тинькофф Инвестиций с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Отправляем запрос на создание нового счета в песочнице
        response = client.sandbox.open_sandbox_account()
        # Получаем идентификатор созданного счета
        account_id = response.account_id
        # Возвращаем сообщение с идентификатором созданного счета
        return "Создан новый аккаунт с id:\n{}".format(account_id)


# Функция для получения списка всех счетов
def get_all_accounts():
    # Создаем объект клиента Тинькофф Инвестиций с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Отправляем запрос на получение списка всех счетов
        accounts = client.users.get_accounts()
    # Получаем список идентификаторов счетов
    account_ids = [account.id for account in accounts.accounts]
    # Если список идентификаторов не пустой, то формируем сообщение со списком идентификаторов
    if account_ids:
        result = "ID ваших аккаунтов:\n" + "\n".join(account_ids)
    # Если список идентификаторов пустой, то формируем сообщение об отсутствии доступных счетов
    else:
        result = "У вас нет доступных аккаунтов."
    # Возвращаем сообщение со списком идентификаторов или сообщением об отсутствии доступных счетов
    return result


# Функция для удаления счета в песочнице
def delete_account(account_id):
    # Создаем объект клиента Тинькофф Инвестиций с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Отправляем запрос на удаление счета в песочнице
        client.sandbox.close_sandbox_account(account_id=account_id)
        # Возвращаем True, если запрос был успешно отправлен
        return True


# Функция для получения данных о валютах
def get_currency_data():
    # Создаем объект клиента Тинькофф Инвестиций с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Отправляем запрос на получение данных о валютах
        currencies = client.instruments.currencies()
    # Создаем пустой список для хранения данных о валютах
    currency_data = []
    # Перебираем все валюты из ответа на запрос
    for currency in currencies.instruments:
        # Если тикер валюты равен 'USD000UTSTOM', 'CNYRUB_TOM' или 'GLDRUB_TOM', то добавляем данные о валюте в список
        if currency.ticker == 'USD000UTSTOM' or currency.ticker == 'CNYRUB_TOM' or currency.ticker == 'GLDRUB_TOM':
            currency_info = (f"{currency.name}\n"
                             f"Возможно совершение операций только на количества ценной бумаги, кратные: "
                             f"{currency.lot}\n"
                             f"Валюта расчетов: {currency.currency}\n"
                             f"Торговая площадка: {currency.exchange}\n"
                             f"Возможность покупки: {'Доступно' if currency.buy_available_flag else 'Недоступно'}\n"
                             f"Возможность продажи: {'Доступно' if currency.sell_available_flag else 'Недоступно'}")
            currency_data.append(currency_info)
    # Возвращаем список с данными о валютах
    return currency_data


# Функция для пополнения счета в песочнице
def credit_account(account_id, units, nano):
    # Создаем объект клиента Тинькофф Инвестиций с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Создаем объект MoneyValue с помощью значений units и nano для указания суммы пополнения
        amount = MoneyValue(units=units, nano=nano, currency='rub')
        # Отправляем запрос на пополнение счета в песочнице
        response = client.sandbox.sandbox_pay_in(account_id=account_id, amount=amount)
        # Получаем новый баланс счета после пополнения
        new_balance = response.balance
        # Возвращаем сообщение с информацией о пополнении и новым балансом счета
        return (
            f"Аккаунт: {account_id}\nПополнен на: {amount.units} рублей {amount.nano} копеек\n"
            f"Новый баланс: {new_balance.units} рублей {new_balance.nano} копеек")


# Получаем информацию о портфеле
def get_info_account(account_id):
    # Создаем объект клиента с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Получаем портфель клиента по его идентификатору
        portfolio = client.operations.get_portfolio(account_id=account_id)
        # Извлекаем общую стоимость портфеля в рублях
        total_amount_portfolio = portfolio.total_amount_portfolio.units
        # Извлекаем текущую относительную доходность портфеля в процентах
        expected_yield = portfolio.expected_yield.units
        # Извлекаем список позиций портфеля
        positions = portfolio.positions
        # Извлекаем список виртуальных позиций портфеля
        virtual_positions = portfolio.virtual_positions
        # Извлекаем общую стоимость акций в портфеле
        total_amount_shares = portfolio.total_amount_shares.units
        # Извлекаем общую стоимость облигаций в портфеле
        total_amount_bonds = portfolio.total_amount_bonds.units
        # Извлекаем общую стоимость фондов в портфеле
        total_amount_etf = portfolio.total_amount_etf.units
        # Извлекаем общую стоимость валют в портфеле
        total_amount_currencies = portfolio.total_amount_currencies.units
        # Извлекаем общую стоимость фьючерсов в портфеле
        total_amount_futures = portfolio.total_amount_futures.units
        # Извлекаем общую стоимость опционов в портфеле
        total_amount_options = portfolio.total_amount_options.units

        return (
                "Общая информация:\n"
                f"Общая стоимость портфеля: {total_amount_portfolio}\n"
                f"Текущая относительная доходность портфеля, в %: {expected_yield}\n"
                "Список позиций портфеля:\n" +
                '\n'.join(
                    f"{position.figi}, {position.instrument_type}, количество: {position.quantity.units}" for position
                    in
                    positions) +
                "\nМассив виртуальных позиций портфеля:\n" +
                '\n'.join(
                    f"{virtual_position.figi}, {virtual_position.instrument_type}, "
                    f"количество: {virtual_position.quantity.units}"
                    for virtual_position in virtual_positions) +
                "\n\nБумаги:\n"
                f"Общая стоимость акций в портфеле: {total_amount_shares}\n"
                f"Общая стоимость облигаций в портфеле: {total_amount_bonds}\n"
                f"Общая стоимость фондов в портфеле: {total_amount_etf}\n"
                f"Общая стоимость валют в портфеле: {total_amount_currencies}\n"
                f"Общая стоимость фьючерсов в портфеле: {total_amount_futures}\n"
                f"Общая стоимость опционов в портфеле: {total_amount_options}"
        )


# Функция для получения списка доступных акций
def get_available_shares():
    # Создаем объект клиента с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Получаем список всех акций
        shares = client.instruments.shares()
        # Создаем пустой список для хранения доступных акций
        available_shares = []
        # Перебираем все акции в списке
        for share in shares.instruments:
            # Если валюта акции - рубли и флаг доступности торговли через API установлен в True, добавляем акцию в 
            # список доступных акций
            if share.currency == 'rub' and share.api_trade_available_flag:
                available_shares.append(share.name)
        # Объединяем список доступных акций в одну строку, разделенную символом переноса строки
        available_shares_str = '\n'.join(available_shares)
        # Возвращаем количество доступных акций и их наименования
        return (f"Количество доступных акций: {len(available_shares)}\n"
                f"Наименование акций:\n"
                f"{available_shares_str}")


# Функция для получения информации об акции
def get_share_data(name):
    # Создаем объект клиента с помощью токена Тинькофф Инвестиций
    with SandboxClient(TOKEN_TIN) as client:
        # Получаем список всех акций
        shares = client.instruments.shares()
        # Перебираем все акции в списке
        for share in shares.instruments:
            # Если наименование акции совпадает с переданным именем, проверяем доступность акции для торговли и 
            # возвращаем информацию об акции
            if share.name == name:
                if share.currency == 'rub' and share.api_trade_available_flag:
                    return (
                        f"Название: {share.name}\n"
                        f"Сектор экономики: {share.sector}\n"
                        f"Figi-идентификатор инструмента: {share.figi}\n"
                        f"Лотность инструмента: {share.lot}\n"
                        f"Коэффициент ставки риска длинной позиции по клиенту: "
                        f"{'Клиент с повышенным уровнем риска' if share.klong.units == 1 else 'Клиент со стандартным уровнем риска'}\n"
                        f"Коэффициент ставки риска короткой позиции по клиенту:"
                        f" {'Клиент с повышенным уровнем риска' if share.kshort.units == 1 else 'Клиент со стандартным уровнем риска'}\n"
                        f"Текущий режим торгов инструмента:"
                        f" {trading_status_map.get(share.trading_status, 'Неизвестный статус')}\n"
                        f"Покупка: {'Доступна' if share.buy_available_flag else 'Недоступна'}\n"
                        f"Продажа: {'Доступна' if share.sell_available_flag else 'Недоступна'}\n"
                        f"Выплата дивидендов: {'Есть' if share.div_yield_flag else 'Нет'}\n")
                else:
                    return "Данная акция недоступна для торгов"


def buy_share(figi, quantity, account_id):
    # Создание клиента для работы с Tinkoff Invest API
    with SandboxClient(TOKEN_TIN) as client:
        # figi, quantity и account_id - это входные параметры функции
        figi = figi
        quantity = quantity
        account_id = account_id
        # order_id - уникальный идентификатор заявки, генерируется с помощью uuid.uuid4()
        order_id = str(uuid.uuid4())
        try:
            # Отправка заявки на покупку акций с помощью метода post_order клиента Tinkoff Invest API
            order = client.orders.post_order(
                figi=figi,
                quantity=quantity,
                account_id=account_id,
                order_id=order_id,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_MARKET,
                instrument_id=figi)

            # Получение статуса исполнения заявки, направления сделки,
            # общей стоимости заявки, комиссии и начальной цены акции
            execution_report_status = EXECUTION_REPORT_STATUS.get(order.execution_report_status, 'Неизвестен')
            direction = ORDER_DIRECTION.get(order.direction, 'Неизвестно')
            total_order_amount_rub = order.total_order_amount.units + order.total_order_amount.nano / 1000000000
            executed_commission_rub = order.executed_commission.units + order.executed_commission.nano / 1000000000
            start_share_price = order.initial_security_price.units + order.initial_security_price.nano / 1000000000

            # Возвращение информации о заявке в виде строки
            return (f"ID заявки: {order.order_id}\n"
                    f"Текущий статус заявки: {execution_report_status}\n"
                    f"Запрошено лотов: {order.lots_requested}\n"
                    f"Исполнено лотов: {order.lots_executed}\n"
                    f"Итоговая стоимость заявки, включающая все комиссии: {total_order_amount_rub:.2f} рублей\n"
                    f"Фактическая комиссия по итогам исполнения заявки: {executed_commission_rub:.2f} рублей\n"
                    f"Направление сделки: {direction}\n"
                    f"Начальная цена за 1 акцию: {start_share_price:.2f} рублей")
        except exceptions.RequestError:
            # Возвращение сообщения об ошибке, если заявка не была исполнена из-за недостатка средств
            return 'Недостаточно средств'


def sell_share(figi, quantity, account_id):
    # Создание клиента для работы с Tinkoff Invest API
    with SandboxClient(TOKEN_TIN) as client:
        # figi, quantity и account_id - это входные параметры функции
        figi = figi
        quantity = quantity
        account_id = account_id
        # order_id - уникальный идентификатор заявки, генерируется с помощью uuid.uuid4()
        order_id = str(uuid.uuid4())
        try:
            # Отправка заявки на продажу акций с помощью метода post_order клиента Tinkoff Invest API
            order = client.orders.post_order(
                figi=figi,
                quantity=quantity,
                account_id=account_id,
                order_id=order_id,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_MARKET,
                instrument_id=figi)

            # Получение статуса исполнения заявки, направления сделки,
            # общей стоимости заявки, комиссии и начальной цены акции

            execution_report_status = EXECUTION_REPORT_STATUS.get(order.execution_report_status, 'Неизвестен')
            direction = ORDER_DIRECTION.get(order.direction, 'Неизвестно')
            total_order_amount_rub = order.total_order_amount.units + order.total_order_amount.nano / 1000000000
            executed_commission_rub = order.executed_commission.units + order.executed_commission.nano / 1000000000
            start_share_price = order.initial_security_price.units + order.initial_security_price.nano / 1000000000

            # Возвращение информации о заявке в виде строки
            return (f"ID заявки: {order.order_id}\n"
                    f"Текущий статус заявки: {execution_report_status}\n"
                    f"Запрошено лотов: {order.lots_requested}\n"
                    f"Исполнено лотов: {order.lots_executed}\n"
                    f"Итоговая стоимость заявки, включающая все комиссии: {total_order_amount_rub:.2f} рублей\n"
                    f"Фактическая комиссия по итогам исполнения заявки: {executed_commission_rub:.2f} рублей\n"
                    f"Направление сделки: {direction}\n"
                    f"Начальная цена за 1 акцию: {start_share_price:.2f} рублей")
        except exceptions.RequestError:
            # Возвращение сообщения об ошибке, если заявка не была исполнена
            return 'Операция не удалась'
