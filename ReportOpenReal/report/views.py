from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
# Create your views here.


class TestEsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = requests.get('http://localhost:9200/addresses/_search')
        # elastic_client = Elasticsearch(hosts=["http://172.16.0.128:9200"])
        # result = elastic_client.search(index="addresses")
        return Response(data=data.json(), status=status.HTTP_200_OK)
