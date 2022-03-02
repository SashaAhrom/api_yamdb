from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, AuthenticationViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(
    'auth', AuthenticationViewSet, basename='get_confirmation_code',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
