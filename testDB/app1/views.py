from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connections
from .helpers import dictfetchall
import requests
from elasticsearch import Elasticsearch
# Create your views here.


class ReportViewSet(viewsets.ViewSet):
    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("select * from IMPORT_2021")
        # report = dictfetchall(cursor=cursor)
        # cursor = cursor.execute("select count(*) from IMPORT_2021")
        # 'report': report
        return Response(data={'data': cursor,
                              }, status=status.HTTP_200_OK)


class TestEsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = requests.get('http://172.16.0.128:9200/addresses/_search')
        elastic_client = Elasticsearch(hosts=["http://172.16.0.128:9200"])
        result = elastic_client.search(index="addresses")
        return Response(data=result, status=status.HTTP_200_OK)
