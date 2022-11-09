from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='report-data', viewset=views.ReportViewSet, basename='report-data')
router.register(prefix='test', viewset=views.TestEsViewSet, basename='test')
urlpatterns = [
    path('', include(router.urls)),
]