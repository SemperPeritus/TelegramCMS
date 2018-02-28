from django.contrib import admin
from django.urls import path, include

import bots.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(bots.urls)),
]
