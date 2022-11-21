from django.shortcuts import render
from elasticsearch_dsl import Q, aggs
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from datetime import datetime
from rest_framework.decorators import action
from .documents import RealEstate2021Document
from .models import RealEstate2021
from .serializers import RealEstate2021Serializer
###############################################################
####        MATH PYTHON                             ##########
#############################################################
from django.db.models import Count, Sum, Avg, Max, Min
from constant.config import MAX_QUERY_REPORT
import statistics as stat
import json
import statistics
# Create your views here.


class TestEsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = requests.get('http://localhost:9200/addresses/_search')
        # elastic_client = Elasticsearch(hosts=["http://172.16.0.128:9200"])
        # result = elastic_client.search(index="addresses")
        return Response(data=data.json(), status=status.HTTP_200_OK)


class ReportDealer(viewsets.ViewSet):

    def get_queryset(self):
        query = RealEstate2021.objects.filter(id__range=(0,MAX_QUERY_REPORT))
        data = self.request.query_params

        city = data.get('city')
        district = data.get('district')
        time = data.get('time')
        st1_quarter = datetime.strptime('2021-1-1', '%Y-%m-%d').date()
        st2_quarter = datetime.strptime('2021-4-1', '%Y-%m-%d').date()
        st3_quarter = datetime.strptime('2021-7-1', '%Y-%m-%d').date()
        st4_quarter = datetime.strptime('2021-10-1', '%Y-%m-%d').date()
        end_quarter = datetime.strptime('2022-1-1', '%Y-%m-%d').date()
        if time:
            print(time)
            if time == '1':
                query = query.filter(ads_date__gte=st1_quarter).filter(ads_date__lt=st2_quarter)
            if time == '2':
                query = query.filter(ads_date__gte=st2_quarter).filter(ads_date__lt=st3_quarter)
            if time == '3':
                query = query.filter(ads_date__gte=st3_quarter).filter(ads_date__lt=st4_quarter)
            if time == '4':
                query = query.filter(ads_date__gte=st4_quarter).filter(ads_date__lt=end_quarter)

            # if time == '4':
            #     query = query.filter('range', ads_date={
            #                          'gte': st4_quarter, 'lt': end_quarter})
                                     
        return query


    @action(methods=['get'], url_path="dealer", detail=False)
    def report_dealer(self, request):
        model = RealEstate2021.objects.filter(id__range=(0, MAX_QUERY_REPORT))
        num_dealer_model = model.filter(dealer_tel__isnull=False)\
            .exclude(dealer_tel='').count()
        # num_dealer = RealEstate2021Document.search().query(
        #     Q('bool', must=[Q('exists', field='dealer_email')])).count()
        # RealEstate2021Document.search().filter
        # num_dealer = RealEstate2021Document.search().update_from_dict({'collapse':{'field':'city'}})
        return Response(data={
            'dealer': 'num_dealer',
            # 'dealer_models': RealEstate2021Serializer(model, many=True, context={'request': request}).data,
            'number': num_dealer_model
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path="activity-dealer", detail=False)
    def activity_dealer(self, request):
        model = RealEstate2021.objects.filter(id__range=(0, MAX_QUERY_REPORT)).filter(dealer_tel__isnull=False)\
            .exclude(dealer_tel='').values_list('dealer_tel', flat=True).order_by('dealer_tel').distinct()
        activities = {}
        for i in range(1, 13):
            count = model.filter(ads_date__month=i).count()
            activities.update({f'T{i}': count})

        return Response(data={
            'total': model.count(),
            'activities': activities
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path="median-re", detail=False)
    def median_re(self, request):

        return Response(data={
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path="price-volatility", detail=False)
    def price_volatility(self, request):
        model = RealEstate2021.objects.filter(id__range=(0, MAX_QUERY_REPORT)).exclude(price=0)\
            .exclude(price__isnull=True).exclude(price__lte=0.01)
        math_price = model.aggregate(Sum('price'), Avg('price'), Max(
            'price'), Min('price'), num_price=Count('price'))
        count_price = model.count()
        percent_price_vol = {}
        price_vol = {}
        for i in range(1, 13):
            price = model.filter(ads_date__month=i).aggregate(Avg('price'))
            price_vol.update({f'T{i}': round(price['price__avg'], 2)})
            percent_price_vol.update(
                {f'T{i}': round((price['price__avg']/math_price['price__avg'])*100, 2)})

        return Response(data={
            'count_price': math_price['num_price'],
            'sum_price': round(math_price['price__sum'], 2),
            'average_price': round(math_price['price__avg'], 2),
            'max_price': round(math_price['price__max'], 2),
            'min_price': round(math_price['price__min'], 2),
            'price_volatility': price_vol,
            'percent_price_volatility': percent_price_vol
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path="price-median", detail=False)
    def price_median(self, request):
        data = self.get_queryset().exclude(price=0).exclude(price__isnull=True)
        price = data.values_list('price', flat=True)
        median_total = statistics.median(price)
        return Response(data={
            'median_total' : median_total
        }, status=status.HTTP_200_OK)
