from django.contrib import admin
from django.urls import path, include

import api.urls
import bots.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api.urls)),
    path('', include(bots.urls))
]
