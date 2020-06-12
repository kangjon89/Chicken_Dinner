from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_lobby),
    path('howto', views.howto),
    path('services', views.services),
    path('strategy', views.strategy),
    path('other', views.other),
]