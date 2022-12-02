from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(prefix='test', viewset=views.TestEsViewSet, basename='test')

router.register(prefix='reports', viewset=views.ReportDealer,
                basename='reports')


urlpatterns = [
    path('', include(router.urls)),
]
