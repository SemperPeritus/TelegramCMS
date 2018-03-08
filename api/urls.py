from django.urls import path, include
from rest_framework import routers

from api.views import BotViewSet, ChannelViewSet, MessageViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bots', BotViewSet)
router.register(r'channels', ChannelViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
