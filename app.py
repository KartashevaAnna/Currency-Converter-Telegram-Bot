import telebot
from config import TOKEN
from utils import ActualConverter, NotDigits, WrongInput, WrongCurrency, TooManyParameters, TooFewParameters


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = """Этот бот конвертирует валюты. Список валют:/currencies. 
    Напишите ему сообщение в таком формате: 
    20 долларов в евро 
    либо 20 USD in EUR
    
    (сколько купили, в какой валюте купили, 
    в какой валюте хотите узнать цену)"""
    bot.reply_to(message, text)
@bot.message_handler(commands=["currencies"])
def currencies(message: telebot.types.Message):
    text = "Available currencies: доллар (USD), евро (EUR), рубли (RUB)"
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def give_exchange_rate(message: telebot.types.Message):
    try:
        text = ActualConverter.reply(message)
    except NotDigits as e:
        bot.reply_to(message, f"This is not a number \n {e}")
    except WrongInput as e:
        bot.reply_to(message, f"Wrong input \n {e}")
    except TooManyParameters as e:
        bot.reply_to(message, f"Too many parameters. Please, see /help\n {e}")
    except TooFewParameters as e:
        bot.reply_to(message, f"Too few parameters. Please, see /help\n {e}")
    except WrongCurrency as e:
        bot.reply_to(message, f"Currency not in the list of currencies, see /help \n {e}")
    except Exception as e:
        bot.reply_to(message, f"We've failed to process your request \n {e}")
    else:
        bot.reply_to(message, text)


bot.polling()





