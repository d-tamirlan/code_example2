from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Wallet:
    EUR: Decimal
    USD: Decimal
    RUB: Decimal
    IDR: Decimal
    CZK: Decimal
