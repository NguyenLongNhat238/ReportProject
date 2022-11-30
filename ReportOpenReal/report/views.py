from django.shortcuts import render
from elasticsearch_dsl import Q, aggs
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from datetime import datetime
from rest_framework.decorators import action

from report.helpers import currency_converter_helper, get_list_district_of_city
from .documents import RealEstate2021Document
from .models import RealEstate2021, RealEstate2022
from .serializers import RealEstate2021Serializer
###############################################################
####        MATH PYTHON                             ##########
#############################################################
from django.db.models import Count, Sum, Avg, Max, Min, Q
from constant.config import CURRENT_UNIT, MAX_QUERY_REPORT, SEARCH_CITY_DISTRICT, UNIT_PRICE, YEAR_OF_REQUEST
import json
import statistics
# Create your views here.


class TestEsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = requests.get('http://localhost:9200/addresses/_search')
        # elastic_client = Elasticsearch(hosts=["http://172.16.0.128:9200"])
        # result = elastic_client.search(index="addresses")
        return Response(data=data.json(), status=status.HTTP_200_OK)


class ReportDealer(viewsets.ViewSet,):

    def get_queryset(self):
        query = RealEstate2022.objects.all()
        data = self.request.query_params

        city = data.get('city')
        district = data.get('district')
        if city:
            query = query.filter(split_city=city)
        if self.action in ['price_median']:
            return query
        if district:
            query = query.filter(split_district=city)
        if self.action in ['price_volatility', 'activity_dealer']:
            print("query price_volatility")
            print(city)
            return query
        
        year = data.get('year')
        time = data.get('time')
        st1_quarter = datetime.strptime(
            f'{YEAR_OF_REQUEST}-1-1', '%Y-%m-%d').date()
        st2_quarter = datetime.strptime(
            f'{YEAR_OF_REQUEST}-4-1', '%Y-%m-%d').date()
        st3_quarter = datetime.strptime(
            f'{YEAR_OF_REQUEST}-7-1', '%Y-%m-%d').date()
        st4_quarter = datetime.strptime(
            f'{YEAR_OF_REQUEST}-10-1', '%Y-%m-%d').date()
        end_quarter = datetime.strptime(
            f'{YEAR_OF_REQUEST}-1-1', '%Y-%m-%d').date()
        if time:
            print(time)
            if time == '1':
                query = query.filter(ads_date__gte=st1_quarter).filter(
                    ads_date__lt=st2_quarter)
            if time == '2':
                query = query.filter(ads_date__gte=st2_quarter).filter(
                    ads_date__lt=st3_quarter)
            if time == '3':
                query = query.filter(ads_date__gte=st3_quarter).filter(
                    ads_date__lt=st4_quarter)
            if time == '4':
                query = query.filter(ads_date__gte=st4_quarter).filter(
                    ads_date__lt=end_quarter)

            # if time == '4':
            #     query = query.filter('range', ads_date={
            #                          'gte': st4_quarter, 'lt': end_quarter})

        return query

    # report Dealer: Số lượng dealer đang hoạt động
    #   - Total_dealer: Tổng số lượng dealer
    #   - num_dealer: số lượng dealer đã đăng bài trong vòng từng quý, từng khu vực
    @action(methods=['get'], url_path="dealer", detail=False)
    def report_dealer(self, request):
        model = self.get_queryset()
        total_dealer = RealEstate2022.objects.filter(dealer_name__isnull=False)\
            .exclude(dealer_name='').values_list('dealer_tel', flat=True).distinct().count()
        number_dealer = model.filter(dealer_name__isnull=False)\
            .exclude(dealer_name='').values_list('dealer_tel', flat=True).distinct().count()
        # num_dealer = RealEstate2021Document.search().query(
        #     Q('bool', must=[Q('exists', field='dealer_email')])).count()
        # RealEstate2021Document.search().filter
        # num_dealer = RealEstate2021Document.search().update_from_dict({'collapse':{'field':'city'}})
        return Response(data={
            'total_dealer': total_dealer,
            'number_dealer': number_dealer
        }, status=status.HTTP_200_OK)

    # Report Hoạt động, số lượng dealer
    #   - số lượng dealer hoạt động trong 12 tháng
    @action(methods=['get'], url_path="activity-dealer", detail=False)
    def activity_dealer(self, request):
        total_ads = RealEstate2022.objects.count()
        total_dealer = RealEstate2022.objects.filter(
            dealer_name__isnull=False).values_list('dealer_tel', flat=True).distinct().count()
        model = self.get_queryset()
        model = model.filter(dealer_name__isnull=False)\
            .exclude(Q(dealer_name='')).values_list('dealer_tel', flat=True).order_by('dealer_tel').distinct()
        # model = RealEstate2022.objects.filter(id__range=(0, MAX_QUERY_REPORT)).filter(dealer_tel__isnull=False)\
        #     .exclude(dealer_tel='').values_list('dealer_tel', flat=True).order_by('dealer_tel').distinct()
        activities = {}
        for i in range(1, 13):
            count = model.filter(ads_date__month=i).count()
            activities.update({f'T{i}': count})

        return Response(data={
            'total_ads': total_ads,
            'total_dealer': total_dealer,
            'activities': activities
        }, status=status.HTTP_200_OK)

    # Report Api Biến động giá theo từng tháng của một năm

    @action(methods=['get'], url_path="price-volatility", detail=False)
    def price_volatility(self, request):
        model = self.get_queryset()
        # model = RealEstate2022.objects.exclude(price=0)\
        #     .exclude(price__isnull=True).exclude(price__lte=0.01)
        model = model.exclude(price=0)\
            .exclude(price__isnull=True).exclude(price__lte=0.01)
        # MATH for price using aggregate in python django
        ###     - average
        ###     - sum
        ###     - max
        ###     - min
        ###     - Count
        math_price = model.aggregate(Sum('price'), Avg('price'), Max(
            'price'), Min('price'), num_price=Count('price'))

        ##### Math price and percent price avg volatility
        percent_price_vol = {}
        price_vol = {}
        for i in range(1, 13):
            ##### Filter ads each month  #########
            price = model.filter(ads_date__month=i).aggregate(Avg('price'))
            #### average price each month ########
            price_vol.update({f'T{i}': currency_converter_helper(price['price__avg'])})

            # average price per month for annual average
            percent_price_vol.update(
                {f'T{i}': round((price['price__avg']/math_price['price__avg'])*100, 2)})

        # return response data :
        #   - count price: count all ads of year
        #   - sum price: sum price of year
        #   - average price: average price of year
        #   - max price: max price of year
        #   - min price: min price of year
        #   - price volatility: list average price each month of year
        #   - percent price volatility: list percent of average price each month of year
        return Response(data={
            'count_price': math_price['num_price'],
            'currency_unit': CURRENT_UNIT,
            'sum_price': currency_converter_helper(math_price['price__sum']),
            'average_price': currency_converter_helper(math_price['price__avg']),
            'max_price': currency_converter_helper(math_price['price__max']),
            'min_price': currency_converter_helper(math_price['price__min']),
            'price_volatility': price_vol,
            'percent_price_volatility': percent_price_vol
        }, status=status.HTTP_200_OK)

    # Report Giá trị trung vị bất động sản
    #   - Lọc theo thành phố, loại bất động sản, theo từng quý
    #   - TÍnh trung vị (Median bằng thư viện statistics) tài sản theo từng quận

    @action(methods=['get'], url_path="price-median", detail=False)
    def price_median(self, request):
        city = self.request.query_params.get('city')
        model = self.get_queryset()
        #### Get list District of city by funtion get_list_district_of_city in helpers.py######
        data = get_list_district_of_city(city)

        ###### MATH median price each district ########
        district = {}
        for i in data:
            values = model.filter(split_district=i["district"]).exclude(price=0)\
                .exclude(price__isnull=True).exclude(price__lte=0.01).values_list('price', flat=True)
            median = 0
            if values:
                median = statistics.median(values)
            #### convert currency: triệu đồng -> tỷ đồng  via funtion currency_converter_helper in helpers.py #####
            district.update(
                {f'{i["district"]}': currency_converter_helper(median)})

        # return response data :
        #   - median each district
        #   - currency unit
        #   - top median
        return Response(data={
            'median_district': district,
            'currency_unit': CURRENT_UNIT,
        }, status=status.HTTP_200_OK)

    # report:
    #   - Số lượng dealer mới
    #   - Số lượng bất động sản rao bán
    #   - Lọc theo từng thành phố, quận, loại bất động sản, từng quý (4 quý)

    @action(methods=['get'], url_name='total-report', detail=False)
    def total_report(self, request):
        pass
