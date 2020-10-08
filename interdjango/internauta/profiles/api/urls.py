from django.contrib import admin
from django.urls import path
from django.conf import settings

from .views import (
    profile_detail_api_view,
    )
#base EndPoint /api/profiles

urlpatterns = [
    path('<str:username>/follow', profile_detail_api_view),
    path('<str:username>/', profile_detail_api_view),

    #url(r'', include('test_app.urls')),
]
