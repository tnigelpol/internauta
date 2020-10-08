"""internauta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nauta.views import (
    text_create_view,
    text_edit_view,
    text_visualize_view,
    add_entry_view,
    retrieve_word_view,
    retrieve_grammars_view,
    add_underline_view,
    text_view,
    homepage_view,
    )

urlpatterns = [
    path('', homepage_view),
    path('admin/', admin.site.urls),
    path('create/', text_create_view),
    path('<int:text_id>/view/', text_visualize_view),
    path('<int:text_id>/edit/', text_edit_view),
    path('<int:text_id>/visualize/', text_view),
    path('add-entry/', add_entry_view),
    path('words/', retrieve_word_view),
    path('<str:lang>/grammar/', retrieve_grammars_view),
    path('add-underline/', add_underline_view),
]
