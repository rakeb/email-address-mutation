from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setparam/', views.set_user_mutation_param, name='setparam'),
    path('sendmail/', views.send_mail, name='sendmail'),
    path('receive/', views.receive_mail, name='receive'),
]