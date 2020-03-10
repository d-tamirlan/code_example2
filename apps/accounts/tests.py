import base64
import unittest

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_dynamic_fixture import G
from apps.accounts.models import Wallet
from .serializers import TransactionSerializer

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.password = '0f9df99b91fc'

        self.sender = G(User, email='some1@yandex.ru', balance=1000, password=make_password(self.password))

        self.recipient = G(User, email='some2@yandex.ru', balance=100)

        self.empty_balance_user = G(User, email='some3@yandex.ru')


@unittest.skip('UserTest skipped')
class UserTest(BaseTestCase):
    def test_empty_balance(self):
        transaction_serializer = TransactionSerializer(data={
                'sender': self.empty_balance_user.pk,
                'recipient': self.recipient.pk,
                'amount': '100',
                'wallet': Wallet.RUB
        })
        self.assertFalse(transaction_serializer.is_valid())


class TransactionsTest(BaseTestCase):
    def test_transfer(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode(f'{self.sender.email}:{self.password}'.encode()),
        }
        response = self.client.post(
            reverse('accounts:transaction'),
            data={
                'sender': self.sender.pk,
                'recipient': self.recipient.pk,
                'amount': '100',
                'wallet': Wallet.USD
            },
            **auth_headers
        )

        self.assertEqual(response.status_code, 201)

        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.empty_balance_user.refresh_from_db()

        self.assertEqual(self.sender.balance, 900)

        self.assertEqual(self.recipient.balance, 200)

