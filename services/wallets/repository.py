from decimal import Decimal
from django.core.cache import cache

import requests
from .models import Wallet


class WalletRepository:
    API_URL = 'https://api.exchangeratesapi.io/latest'

    @staticmethod
    def _get_wallets_from_api(base) -> dict:
        response = requests.get(
            WalletRepository.API_URL,
            params={'base': base, 'symbols': 'EUR,USD,IDR,RUB,CZK'}
        )
        return response.json()

    @staticmethod
    def get_wallets(base) -> Wallet:
        wallets_json = cache.get('wallets_json')

        if not wallets_json:
            wallets_json = WalletRepository._get_wallets_from_api(base)

            wallets_json = {k: Decimal(v) for k, v in wallets_json['rates'].items()}

            # Кэшируем на 3 минуты
            cache.set('wallets_json', wallets_json, timeout=60*3)

        wallets = Wallet(**wallets_json)

        return wallets
