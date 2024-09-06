import telebot
from config import values, TOKEN
from extensions import APIExeptions, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def instruction(message: telebot.types.Message):
    instructions = ('Добро пожаловать в конвертер валют написаный на языке Python!!!\n'
'Узнать все доступные валюты можно командой /values\n'
'Чтобы конвертировать валюту введите данные в формате:\n'
'<количество первой валюты> <имя валюты, цену которой вы хотите узнать> <имя валюты, в которой нужно узнать цену первой валюты>')
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def values_(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in values:
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter__(message: telebot.types.Message):

    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIExeptions('Количество параметров должно быть равно 3!')

        amount, base, quote = value
        total_base = Converter.get_price(amount, base, quote)
    except APIExeptions as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.send_message(f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_base * int(amount)}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
