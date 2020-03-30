from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Wallet:
    EUR = 'EUR'
    USD = 'USD'
    IDR = 'IDR'
    RUB = 'RUB'
    CZK = 'CZK'

    CHOICES = (
        (EUR, 'Евро'),
        (USD, 'Доллары'),
        (RUB, 'Рубли'),
        (CZK, 'Кроны'),
        (IDR, 'Рупии'),
    )


class User(AbstractUser):
    email = models.EmailField('E-mail адрес', unique=True, error_messages={
            'unique': 'Пользователь с такой почтой уже существует',
        })
    balance = models.DecimalField('Баланс', max_digits=100, decimal_places=2, default=0)
    wallet = models.CharField('Валюта', max_length=3, choices=Wallet.CHOICES, default=Wallet.USD)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.username = self.email
        return super().save()


class Transaction(models.Model):
    sender = models.ForeignKey(User, verbose_name='Отправитель', related_name='debit', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, verbose_name='Получатель', related_name='enrollment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    wallet = models.CharField('Валюта', max_length=3, choices=Wallet.CHOICES, default='')
    date = models.DateTimeField('Дата', auto_now_add=True)

    def clean(self):
        if self.sender == self.recipient:
            raise ValidationError('Отправитель и получатель не должны совпадать')

        return super().clean()
