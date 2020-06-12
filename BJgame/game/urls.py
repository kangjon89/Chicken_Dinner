from django.urls import path
from . import views

urlpatterns = [
    path('', views.game),
    path('/result',views.result),
    path('/gameover',views.gameover),
]
