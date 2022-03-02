from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (ConfirmationCodeSerializer, JwtTokenSerializer,
                          UserSerializer, AdminSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class AuthenticationViewSet(viewsets.GenericViewSet):

    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action =='send_confirmation_code':
            return ConfirmationCodeSerializer
        return JwtTokenSerializer

    @action(
        methods=['post'], detail=False, url_path='signup', url_name='signup',
    )
    def send_confirmation_code(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user, created = User.objects.get_or_create(
                username=username, email=email,
            )
            code = user.confirmation_code
            confirmation_email = EmailMessage(
                subject='Код подтвеждения',
                body=f'Ваш код для авторизации на сайте YaMDB: {code}',
                from_email='noreply@yamdb.ru',
                to=[email],
            )
            confirmation_email.send()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='token', url_name='token')
    def get_jwt_token(self, request):
        serializer = JwtTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            code = serializer.validated_data.get('confirmation_code')
            user = get_object_or_404(
                User, username=username, confirmation_code=code,
            )
            token = RefreshToken.for_user(user)
            user.is_active = True
            return Response(
                data={'access': str(token.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
