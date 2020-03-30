from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.serializers import raise_errors_on_nested_writes

from services.wallets.repository import WalletRepository
from .models import Transaction

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class TransactionSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        sender = attrs['sender']
        amount = attrs['amount']

        if sender.balance < amount:
            raise serializers.ValidationError({'sender': 'Недостаточно средств на счету'})

        if amount <= 0:
            raise serializers.ValidationError({'amount': 'Сумма должна быть больше нуля'})

        return attrs

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        instance = self.Meta.model(**validated_data)

        wallets = WalletRepository.get_wallets(instance.wallet)

        sender_wallet = getattr(wallets, instance.sender.wallet) * instance.amount

        recipient_wallet = getattr(wallets, instance.recipient.wallet) * instance.amount

        instance.sender.balance -= sender_wallet
        instance.recipient.balance += recipient_wallet

        with transaction.atomic():
            instance.sender.save()
            instance.recipient.save()
            instance.save()

        return instance

    class Meta:
        model = Transaction
        fields = ('sender', 'recipient', 'amount', 'wallet')
        extra_kwargs = {
            'amount': {'required': True},
            'wallet': {'required': True}
        }
