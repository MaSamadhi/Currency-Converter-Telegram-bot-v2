import telebot
from config import TOKEN, currencies
from exceptions import APIException, CrypConverter

bot = telebot.TeleBot(TOKEN)

help_text = '''Этот бот — конвертер валют.

Чтобы начать работу, введите команду боту в следующем формате:
<Имя валюты> <В какую валюту перевести> <Количество переводимой валюты> 
Например, если Вы хотите перевести 100 долларов в рубли, запрос должен выглядеть как "доллар рубль 100".

Посмотреть список доступных валют: /values'''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}!\n\n{help_text}')

@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['values'])
def values(message):
    values_text = 'Доступные валюты:'
    for currency, value in currencies.items():
        values_text = '\n'.join((values_text, f'{currency} {value[1]}',))
    bot.send_message(message.chat.id, values_text)

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.title().split()
        print(values)
        if len(values) != 3:
            raise APIException('Слишком много параметров!')

        curr1, curr2, amount = values
        base = CrypConverter.convert(curr1, curr2, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        convert_text = f'{amount} {currencies[curr1][0]} = {base * float(amount)} {currencies[curr2][0]}'
        bot.send_message(message.chat.id, convert_text)


bot.polling(none_stop=True)