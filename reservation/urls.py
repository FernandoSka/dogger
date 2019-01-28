"""dogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from .views import (
    ReservationCreate,
    AddDogItem,
    ReservationDetail,
    AcceptReservation,
    RefuseReservation,
    CancelReservation,
    ConcludeReservation,
)

urlpatterns = [
    path('reservation', ReservationCreate.as_view(), name='reservation_create'),
    path('reservation_detail', ReservationDetail.as_view(), name='reservation_detail'),
    path('reservation_detail/<slug:pk>', ReservationDetail.as_view(), name='reservation_detail'),
    path('reservation_detail/<slug:pk>/accept', AcceptReservation.as_view(), name='reservation_accept'),
    path('reservation_detail/<slug:pk>/refuse', RefuseReservation.as_view(), name='reservation_refuse'),
    path('reservation_detail/<slug:pk>/cancel', CancelReservation.as_view(), name='reservation_cancel'),
    path('reservation_detail/<slug:pk>/conclude', ConcludeReservation.as_view(), name='reservation_conclude'),
    path('reservation/items', AddDogItem.as_view(), name='reservation_detail'),
]