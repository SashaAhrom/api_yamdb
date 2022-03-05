from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (AdminSerializer, ConfirmationCodeSerializer,
                          JwtTokenSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for users/."""

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
        """
        View for users/me. Allows any authenticated user access and
        patch it's profile.
        """
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
    """Viewset for registering and authenticating users."""

    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """Returns serializer class depending on which view is used."""
        if self.action == 'send_confirmation_code':
            return ConfirmationCodeSerializer
        return JwtTokenSerializer

    def send_email(self, user: User):
        """Sends confirmation code to user."""
        subject = 'Код подтвеждения'
        body = '''
        Ваш код для авторизации на сайте YaMDB: {code}
        Ваше имя пользователя: {username}'''
        from_email = 'noreply@yamdb.ru'
        code = user.confirmation_code
        email = user.email
        username = user.username
        confirmation_email = EmailMessage(
            subject=subject,
            body=body.format(code=code, username=username),
            from_email=from_email,
            to=[email],
        )
        confirmation_email.send()

    @action(
        methods=['post'], detail=False, url_path='signup', url_name='signup',
    )
    def send_confirmation_code(self, request):
        """
        View for signing up new user. If user was already created
        sends new email with confirmation code.
        """
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
        except User.DoesNotExist:
            pass
        else:
            self.send_email(user)
            data = {'email': user.email, 'username': user.username}
            return Response(data=data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user, created = User.objects.get_or_create(
                username=username, email=email,
            )
            self.send_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='token', url_name='token')
    def get_jwt_token(self, request):
        """View for refreshing jwt access token for registered user."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            code = serializer.validated_data.get('confirmation_code')
            user = get_object_or_404(
                User, username=username, confirmation_code=code,
            )
            token = RefreshToken.for_user(user)
            return Response(
                data={'access': str(token.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)