import decimal
import logging
import argparse

# Настройки логирования
logging.basicConfig(
    filename='bank_operations.log',
    filemode='a',  # 'a' для добавления в конец файла
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

MULTIPLICITY = 50
PERCENT_REMOVAL = decimal.Decimal(15) / decimal.Decimal(1000)
MIN_REMOVAL = decimal.Decimal(30)
MAX_REMOVAL = decimal.Decimal(600)
PERCENT_DEPOSIT = decimal.Decimal(3) / decimal.Decimal(100)
COUNTER4PERCENTAGES = 3
RICHNESS_PERCENT = decimal.Decimal(10) / decimal.Decimal(100)
RICHNESS_SUM = decimal.Decimal(10_000_000)

bank_account = decimal.Decimal(0)
count = 0
operations = []

def check_multiplicity(amount):
    if (amount % MULTIPLICITY) != 0:
        logging.error(f'Сумма должна быть кратной {MULTIPLICITY} у.е.')
        return False
    return True

def deposit(amount):
    global bank_account, count
    if not check_multiplicity(amount):
        logging.info(f'Сумма должна быть кратной {MULTIPLICITY} у.е.')
        return False
    count += 1
    bank_account += amount
    operations.append(f'Пополнение карты на {amount} у.е. Итого {bank_account} у.е.')
    logging.info(f'Пополнение карты на {amount} у.е. Итого {bank_account} у.е.')
    return True

def withdraw(amount):
    global bank_account, count
    percent = amount * PERCENT_REMOVAL
    percent = MIN_REMOVAL if percent < MIN_REMOVAL else MAX_REMOVAL if percent > MAX_REMOVAL else percent
    if bank_account >= amount + percent:
        count += 1
        bank_account -= (amount + percent)
        operations.append(f'Снятие с карты {amount} у.е. Процент за снятие {int(percent)} у.е.. Сумма на карте {int(bank_account)} у.е.')
        logging.info(f'Снятие с карты {amount} у.е. Процент за снятие {int(percent)} у.е.. Сейчас на карте осталось {int(bank_account)} у.е.')
    else:
        operations.append(f'Недостаточно средств. Сумма с комиссией {amount + int(percent)} у.е. На карте {int(bank_account)} у.е.')
        logging.error(f'Недостаточно средств на счете. На карте - {int(bank_account)} у.е., а сумма снятия с комиссией {amount + int(percent)} у.е.')

def exit():
    global bank_account, operations
    if bank_account > RICHNESS_SUM:
        percent = bank_account * RICHNESS_PERCENT
        bank_account -= percent
        operations.append(f'Вычтен налог на богатство {RICHNESS_PERCENT*100}% в сумме {percent} у.е. Итого {bank_account} у.е.')
        logging.info(f'Вычтен налог на богатство {RICHNESS_PERCENT*100}% в сумме {percent} у.е. Итого {bank_account} у.е.')
    operations.append(f'Возьмите карту на которой {bank_account} у.е.')

def main(deposit_amount, withdraw_amount):
    deposit(decimal.Decimal(deposit_amount))
    withdraw(decimal.Decimal(withdraw_amount))
    exit()
    for op in operations:
        print(op)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Обработка банковских операций.')
    parser.add_argument('--deposit', type=float, help='Сумма для пополнения', default=0)
    parser.add_argument('--withdraw', type=float, help='Сумма для снятия', default=0)
    args = parser.parse_args()
    main(args.deposit, args.withdraw)