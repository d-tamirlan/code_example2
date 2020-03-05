import base64

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.accounts.models import Wallet
from .serializers import TransactionSerializer

User = get_user_model()


class UserTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user('some1@yandex.ru', password='0f9df99b91fc', email='some1@yandex.ru',
                                               balance=1000, wallet=Wallet.RUB)
        self.recipient = User.objects.create_user('some2@yandex.ru', password='0f9df99b91fc', email='some2@yandex.ru',
                                                  balance=100, wallet=Wallet.RUB)
        self.empty_balance_user = User.objects.create_user('some3@yandex.ru', password='0f9df99b91fc',
                                                           email='some3@yandex.ru', wallet=Wallet.RUB)

    def test_empty_balance(self):
        transaction_serializer = TransactionSerializer(data={
                'sender': self.empty_balance_user.pk,
                'recipient': self.recipient.pk,
                'amount': '100',
                'wallet': Wallet.RUB
        })
        self.assertFalse(transaction_serializer.is_valid())


class TransactionsTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user('some1@yandex.ru', password='0f9df99b91fc', email='some1@yandex.ru',
                                               balance=1000, wallet=Wallet.RUB)
        self.recipient = User.objects.create_user('some2@yandex.ru', password='0f9df99b91fc', email='some2@yandex.ru',
                                                  balance=100, wallet=Wallet.RUB)
        self.empty_balance_user = User.objects.create_user('some3@yandex.ru', password='0f9df99b91fc',
                                                           email='some3@yandex.ru', wallet=Wallet.RUB)

    def test_transfer(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode(b'some1@yandex.ru:0f9df99b91fc'),
        }
        response = self.client.post(
            reverse('accounts:transaction'),
            data={
                'sender': self.sender.pk,
                'recipient': self.recipient.pk,
                'amount': '100',
                'wallet': Wallet.RUB
            },
            **auth_headers
        )

        self.assertEqual(response.status_code, 201)

        self.sender.refresh_from_db()
        self.recipient.refresh_from_db()
        self.empty_balance_user.refresh_from_db()

        self.assertEqual(self.sender.balance, 900)

        self.assertEqual(self.recipient.balance, 200)

