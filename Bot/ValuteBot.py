import telebot
from Config import keys, TOKEN
from extensions import ConvertionException, ValuteConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = "Чтобы начать работу, введите команды боту в следующем порядке с заглавной буквы в одну строку через пробел:\n1.Имя валюты, цену которой хотите узнать.\
    \n2.Имя валюты, в которую необходимо конвертировать введённую ранее валюту.\
    \n3.Количество конвертируемой валюты. \n\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)
       
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try: 
        values = message.text.split(' ')
   
        if len(values) != 3:
            raise ConvertionException('Cлишком много параметров.')
        
        quote, base, amount = values
        total_base = ValuteConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
     
bot.polling()


