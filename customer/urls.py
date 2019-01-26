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
	CreateWalker,
	CreateOwner,
	WalkerDashboard,
	WalkerList,
	OwnerDog,
	OwnerDashboard
)

urlpatterns = [
    path('sign_walker', CreateWalker.as_view(), name='create_walker'),
    path('sign_owner', CreateOwner.as_view(), name='create_walker'),
    path('walker', WalkerDashboard.as_view(), name='walker_detail'),
    path('owner', OwnerDashboard.as_view(), name='owner_detail'),
    path('walker_list', WalkerList.as_view(), name='walker_list'),
    path('dog_list', OwnerDog.as_view(), name='dog_list'),
]
