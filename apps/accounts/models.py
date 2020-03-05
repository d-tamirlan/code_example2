from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Wallet:
        EUR = 'EUR'
        USD = 'USD'
        GPB = 'GPB'
        RUB = 'RUB'
        BTC = 'BTC'

        CHOICES = (
            (EUR, 'Евро'),
            (USD, 'Доллары'),
            (GPB, 'Фунт стерлингов'),
            (RUB, 'Рубли'),
            (BTC, 'Биткоины'),
        )

    email = models.EmailField('E-mail адрес', unique=True, error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        })
    balance = models.DecimalField('Баланс', max_digits=100, decimal_places=2, default=0)
    wallet = models.CharField('Валюта', max_length=3, choices=Wallet.CHOICES, default=Wallet.USD)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save()
