from django.urls import path

from . import views

urlpatterns = [
    path('vaccine/cert/verify/<str:uuid>', views.index, name='index'),
]
