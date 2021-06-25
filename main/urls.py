from django.urls import path

from . import views

urlpatterns = [
    path('vaccine/cert/verify/<str:uuid>', views.vaccine_page, name='vaccine_page'),
    path('', views.index, name='index')
]
