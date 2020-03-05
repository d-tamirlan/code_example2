from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

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

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)

        instance.sender.balance -= instance.amount
        instance.recipient.balance += instance.amount

        instance.sender.save()
        instance.recipient.save()

        return instance

    class Meta:
        model = Transaction
        fields = ('sender', 'recipient', 'amount')
        extra_kwargs = {'amount': {'required': True}}
