from random import choice

from django.core.mail import EmailMessage
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import ConfirmationCodeSerializer, UserSerializer


class CreateDestroyListRetrieveViewSet(mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       viewsets.GenericViewSet):
    pass


class UserViewSet(CreateDestroyListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=True,
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
        