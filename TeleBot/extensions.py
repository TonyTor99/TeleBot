import requests
import json
from config import values


class APIExeptions(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(amount, base, quote):

        if base == quote:
            raise APIExeptions('Нельзя конвертировать одинаковые валюты')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIExeptions(f'Я не могу конвертировать валюту {base}')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIExeptions(f'Я не могу конвертировать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeptions(f'Количество валют должно быть числом')

        if amount <= 0:
            raise APIExeptions(f'Количество валют должно быть больше 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')

        total_base = json.loads(r.content)[values[quote]]
        return total_base
