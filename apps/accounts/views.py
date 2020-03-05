from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import CreateAPIView, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, TransactionSerializer

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class TransactionView(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    # def post(self, request):
    #     user_from = get_object_or_404(User, email=request.data.get('user_from_email'))
    #     user_to = get_object_or_404(User, email=request.data.get('user_to_email'))
    #     amount = request.data.get('amount')
    #
    #     print(user_from)
    #     print(user_to)
    #     return Response({
    #         'email': request.user.email,  # `django.contrib.auth.User` instance.
    #         'auth': request.auth,  # None
    #     })
