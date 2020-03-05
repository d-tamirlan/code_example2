from django.db.models import Q
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, TransactionSerializer
from .models import Transaction

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class TransactionView(ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        return Transaction.objects.filter(Q(sender_id=user_id) | Q(recipient_id=user_id))
