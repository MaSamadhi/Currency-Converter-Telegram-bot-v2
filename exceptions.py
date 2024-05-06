import requests
import json
from config import currencies

class APIException(Exception):
    pass

class CrypConverter:
    @staticmethod
    def convert(curr1: str, curr2: str, amount: str):

        if curr1 == curr2:
            raise APIException(f'Одинаковые валюты {curr1}!')

        try:
            curr1_ticker = currencies[curr1][0]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {curr1}')

        try:
            curr2_ticker = currencies[curr2][0]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту {curr2}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Невозможно обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={curr1_ticker}&tsyms={curr2_ticker}')
        base = json.loads(r.content)[currencies[curr2][0]]

        return base