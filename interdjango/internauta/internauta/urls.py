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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from nauta import views
from nauta.views import (
    text_create_view,
    text_edit_view,
    text_visualize_view,
    # text_tr_view,
    # text_visualizetr_view,
    add_entry_view,
    retrieve_word_view,
    retrieve_grammars_view,
    add_underline_view,
    text_view,
    text_delete,
    homepage_view,
    user_feed_view,
    global_feed_view,
    # search,
    # text,
    index,
    feed,
    search,
    update,
    )
from accounts.views import (
    login_view,
    logout_view,
    register_view
)

urlpatterns = [
    # path('', homepage_view),
    path('', index),
    path('feed/', feed, name='text-list'),
    path('search/', search, name='search'),
    path('<int:text_id>/update/', update, name='update'),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('create/', text_create_view),
    # APIs
    re_path(r'profiles?/', include('profiles.urls')),
    re_path(r'api/profiles?/', include('profiles.api.urls')),
    path('<int:text_id>/view/', views.text_visualize_view, name='view'),
    path('<int:text_id>/edit/', views.text_edit_view, name='edit'),
    # path('<int:text_id>/tr/', views.text_tr_view, name='tr'),
    # path('<int:text_id>/viewTrans/', views.text_visualizetr_view, name='viewtr'),
    path('<int:text_id>/delete/', views.text_delete, name='delete'),
    path('<int:text_id>/visualize/', text_view, name='visualize'),
    path('add-entry/', add_entry_view),
    path('words/', views.retrieve_word_view),
    path('<str:lang>/grammar/', retrieve_grammars_view),
    path('add-underline/', add_underline_view),
    path('feed/', user_feed_view, name="home-view"),
    path('global/', global_feed_view),
    # path('search/', search, name='search'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)