from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(prefix='test', viewset=views.TestEsViewSet, basename='test')

router.register(prefix='reports', viewset=views.ReportDealer,
                basename='reports')

router.register(prefix='real-estate-2022',
                viewset=views.RealEstate2022ViewSet, basename='real-estate-2022')

urlpatterns = [
    path('', include(router.urls)),
]
