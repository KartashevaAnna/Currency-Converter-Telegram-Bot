import requests
import json
import telebot
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

class WrongInput(Exception):
    pass
class NotDigits(WrongInput):
    pass
class TooManyParameters(WrongInput):
    pass
class TooFewParameters(WrongInput):
    pass
class WrongCurrency(WrongInput):
    pass

class ActualConverter:
    @staticmethod
    def reply(message: telebot.types.Message):
        split = message.text.split()
        if len(split) > 4:
            raise TooManyParameters("Too many parameters. Please, consult /help")
        if len(split) < 4:
            raise TooFewParameters("Too few parameters. Please, consult /help")
        amount = split[0]
        if not amount.isdigit():
            raise NotDigits("Please specify the amount")
        amount = float(amount)
        from_currency, to_currency = split[1], split[3]
        if from_currency in keys:
            from_currency = keys[from_currency]
        else:
            raise WrongCurrency("currency not in the list of currencies")
        if to_currency in keys:
            to_currency = keys[to_currency]
        else:
            raise WrongCurrency("currency not in the list of currencies")

        text = (amount * ActualConverter.conversion(from_currency, to_currency))
        text = str(text)
        return text

    @staticmethod
    def conversion(from_currency, to_currency):
        from_currency = ActualConverter.current_exchange_rates()["rates"][from_currency]
        to_currency = ActualConverter.current_exchange_rates()["rates"][to_currency]
        return round(to_currency/from_currency, 2)

    @staticmethod
    def current_exchange_rates():
        r = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=b468c6f2cc3295c1760f81d58be6ddc0")
        dictionary_with_exchange_rates = json.loads(r.content)
        return dictionary_with_exchange_rates