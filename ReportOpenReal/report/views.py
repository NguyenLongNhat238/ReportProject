from django.shortcuts import render
from elasticsearch_dsl import Q, aggs
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from datetime import datetime
from rest_framework.decorators import action

from report.helpers import currency_converter_helper, get_data_vs_map_district_of_city, get_list_district_of_city, get_list_ward_of_district, get_month_params_for_query, get_year_params, get_year_query_drf, valid_year_uda
from report.paginations import RealEstate2022Paginator
from .documents import RealEstate2021Document
from .models import RealEstate2021, RealEstate2022
from .serializers import RealEstate2021Serializer, RealEstate2022Serializer, ReportParamsValidateExportSerializer, ReportParamsValidateSerializer
###############################################################
####        MATH PYTHON                             ##########
#############################################################
from django.db.models import Count, Sum, Avg, Max, Min, Q
from constant.config import CURRENT_UNIT, MAX_QUERY_REPORT, UNIT_PRICE, YEAR_OF_REQUEST
from constant.res_handing import ErrorHandling
import json
import statistics
# Create your views here.


class TestEsViewSet(viewsets.ViewSet):
    def list(self, request):
        data = requests.get('http://172.16.1.27:9200/addresses/_search')
        # elastic_client = Elasticsearch(hosts=["http://172.16.0.128:9200"])
        # result = elastic_client.search(index="addresses")
        return Response(data=data.json(), status=status.HTTP_200_OK)


class ReportDealer(viewsets.ViewSet,):

    def get_params(self):
        data = self.request.query_params
        params = data
        # city = data.get('city')
        # district = data.get('district')
        # ward = data.get('ward')
        # street = data.get('street') 
        # from_date = data.get('from_date')
        # to_date = data.get('to_date')
        # params = {}
        # if city:
        #     params.update({'city': city})
        # if district:
        #     params.update({'district': district})
        # if ward:
        #     params.update({'ward': ward})
        # if street:
        #     params.update({'street': street})
        # if from_date:
        #     params.update({'from_date': from_date})
        # if to_date:
        #     params.update({'to_date': to_date})
        return params

    def get_queryset(self):
        data = self.request.query_params
        # validate params
        if self.action not in ['total_report']:
            serializer = ReportParamsValidateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        # params
        year = get_year_query_drf(data.get('year'))
        city = data.get('city')
        district = data.get('district')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        ward = data.get('ward')
        street = data.get('street')
        if year == 2022:

            query = query_total = RealEstate2022.objects.all()
        # elif year == 2021:
        #     query_total = RealEstate2021.objects.all()
        #     query = RealEstate2021.objects.all()
        else:
            query = query_total = RealEstate2022.objects.all()

        if city:
            query = query.filter(split_city=city)
        if self.action not in ['price_per_district', 'district_of_interest', 'places_of_interest']:
            if district:
                query = query.filter(split_district=district)
            if ward:
                query = query.filter(split_ward=ward)
            if street:
                query = query.filter(format_street=street)

        if from_date:
            query = query.filter(ads_date__gte=from_date)
        if to_date:
            query = query.filter(ads_date__lte=to_date)
        # if self.action in ['activity_dealer']:
        #     return query, query_total

        return query, query_total

    # report Dealer: S??? l?????ng dealer ??ang ho???t ?????ng
    #   - Total_dealer: T???ng s??? l?????ng dealer
    #   - num_dealer: s??? l?????ng dealer ???? ????ng b??i trong v??ng t???ng qu??, t???ng khu v???c
    @action(methods=['get'], url_path="dealer", detail=False)
    def report_dealer(self, request):
        model, query_total = self.get_queryset()
        num_ads = model.count()
        # ads_street = []
        # for i in num_ads:
        #     ads_street.append(i.format_street)
        total_dealer = query_total.filter(dealer_name__isnull=False)\
            .exclude(dealer_name='').values_list('dealer_tel', flat=True).distinct().count()

        number_dealer = model.filter(dealer_name__isnull=False)\
            .exclude(dealer_name='').values_list('dealer_tel', flat=True).distinct().count()
        # num_dealer = RealEstate2021Document.search().query(
        #     Q('bool', must=[Q('exists', field='dealer_email')])).count()
        # RealEstate2021Document.search().filter
        # num_dealer = RealEstate2021Document.search().update_from_dict({'collapse':{'field':'city'}})
        return Response(data={
            'total_dealer': total_dealer,
            'number_ads': num_ads,
            'number_dealer': number_dealer,
            'params': self.get_params(),
        }, status=status.HTTP_200_OK)

    # Report Ho???t ?????ng, s??? l?????ng dealer
    #   - s??? l?????ng dealer ho???t ?????ng trong 12 th??ng
    @action(methods=['get'], url_path="activity-dealer", detail=False)
    def activity_dealer(self, request):
        # Get query set
        model, query_total = self.get_queryset()
        total_ads = query_total.count()
        total_dealer = query_total.filter(
            dealer_name__isnull=False).values_list('dealer_tel', flat=True).distinct().count()
        model = model.filter(dealer_name__isnull=False)\
            .exclude(Q(dealer_name='')).values_list('dealer_tel', flat=True).order_by('dealer_tel').distinct()
        number_activities_dealer = model.count()
        # model = RealEstate2022.objects.filter(id__range=(0, MAX_QUERY_REPORT)).filter(dealer_tel__isnull=False)\
        #     .exclude(dealer_tel='').values_list('dealer_tel', flat=True).order_by('dealer_tel').distinct()
        activities = {}
        for i in range(1, 13):
            count = model.filter(ads_date__month=i).count()
            if count:
                activities.update({f'T{i}': count})

        return Response(data={
            'total_ads': total_ads,
            'total_dealer': total_dealer,
            'number_activities_dealer': number_activities_dealer,
            'total_ads_per_month': activities,
            'params': self.get_params(),
        }, status=status.HTTP_200_OK)

    # Report Api Bi???n ?????ng gi?? theo t???ng th??ng c???a m???t n??m

    @action(methods=['get'], url_path="price-volatility", detail=False)
    def price_volatility(self, request):
        model, query_total = self.get_queryset()
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
        if model.count() < 10:
            return Response(ErrorHandling(message='Hi???n ch??a c???p nh???t d??? li???u v??? v??? tr?? v?? th???i gian n??y / This location and time data has not been updated yet',
                                          code='NONE VALUE', type='NONE VALUE', lang='vi').to_representation(), status=status.HTTP_200_OK)
        math_price = model.aggregate(Sum('price'), Avg('price'), Max(
            'price'), Min('price'), num_price=Count('price'))

        # Math price and percent price avg volatility
        percent_price_vol = {}
        price_vol = {}
        for i in range(1, 13):
            ##### Filter ads each month  #########
            price = model.filter(ads_date__month=i).aggregate(Avg('price'))
            #### average price each month ########
            if price['price__avg']:
                price_vol.update(
                    {f'T{i}': currency_converter_helper(price['price__avg'])})

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
            'percent_price_volatility': percent_price_vol,
            'params': self.get_params(),
        }, status=status.HTTP_200_OK)

    # Report Gi?? tr??? trung v??? b???t ?????ng s???n
    #   - L???c theo th??nh ph???, lo???i b???t ?????ng s???n, theo t???ng qu??
    #   - T??nh trung v??? (Median b???ng th?? vi???n statistics) t??i s???n theo t???ng qu???n

    @action(methods=['get'], url_path="price-per-district", detail=False)
    def price_per_district(self, request):
        city = self.request.query_params.get('city')
        model, query_total = self.get_queryset()
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
            #### convert currency: tri???u ?????ng -> t??? ?????ng  via funtion currency_converter_helper in helpers.py #####
            district.update(
                {f'{i["district"]}': currency_converter_helper(median)})

        # return response data :
        #   - median each district
        #   - currency unit
        #   - top median
        return Response(data={
            'price_per_district': district,
            'currency_unit': CURRENT_UNIT,
            'params': self.get_params(),
        }, status=status.HTTP_200_OK)

    # report:
    #   - S??? l?????ng dealer m???i
    #   - S??? l?????ng b???t ?????ng s???n rao b??n
    #   - L???c theo t???ng th??nh ph???, qu???n, lo???i b???t ?????ng s???n, t???ng qu?? (4 qu??)

    @action(methods=['get'], url_path='total-report', detail=False)
    def total_report(self, request):
        month_now = datetime.now().date().month
        year_now = datetime.now().date().year
        model, query_total = self.get_queryset()
        # query_total = query_total.filter(ads_date__year=year_now)
        new_ads = query_total.filter(ads_date__month=month_now).count()
        dealer_in_month = query_total.filter(
            ads_date__month=month_now).values_list('dealer_tel', flat=True)
        dealer_befor = query_total.filter(ads_date__month__lt=month_now).filter(
            dealer_tel__in=dealer_in_month).values_list('dealer_tel', flat=True)
        new_dealer = query_total.filter(ads_date__month=month_now).exclude(dealer_tel__in=dealer_befor)\
                                .values_list('dealer_tel').distinct().count()
        return Response(data={
            'new_dealer': new_dealer,
            'new_ads': new_ads,
            # 'params': self.get_params(),
        })

    @action(methods=['get'], url_path='district-of-interest', detail=False)
    def district_of_interest(self, request):
        model, query_total = self.get_queryset()
        city = self.request.query_params.get('city')
        data, data_map = get_data_vs_map_district_of_city(city)
        district = []
        total_ads = query_total.count()
        total_ads_of_city = model.count()
        for i in data:
            values = model.filter(split_district=i["district"]).count()
            # lat, lon = None, None
            # if ('lat' and 'lon') in i.keys():
            #     lat, lon = i['lat'], i['lon']
            #### total ads perdistrict #####
            district.append({
                'id': i['id'],
                'name': i['district'],
                'values': values,
            })
        return Response(data={
            'total_ads': total_ads,
            'total_city_ads': total_ads_of_city,
            'ads_per_district': district,
            'data_map': data_map,
            'params': self.get_params(),
        })

    @action(methods=['get'], url_path='ward-of-interest', detail=False)
    def ward_of_interest(self, request):
        model, query_total = self.get_queryset()
        city = self.request.query_params.get('city')
        district = self.request.query_params.get('district')
        data = get_list_ward_of_district(city=city, district=district)
        ward = []
        total_ads = query_total.count()
        total_district_ads = model.count()
        for i in data:
            # if 'ward' in i:
            values = model.filter(split_ward=i["ward"]).count()
            # lat, lon = None, None
            # if ('lat' and 'lon') in i.keys():
            #     lat, lon = i['lat'], i['lon']
            #### total ads perdistrict #####
            ward.append({
                'id': i['id'],
                'name': i['ward'],
                'values': values,
                # 'coordinates': [[lat, lon]]
            })
        return Response(data={
            'total_ads': total_ads,
            'total_district_ads': total_district_ads,
            'ads_per_ward': ward,
            'params': self.get_params(),
        })

    @action(methods=['get'], url_path='places-of-interest', detail=False)
    def places_of_interest(self, request):
        model, query_total = self.get_queryset()
        city = self.request.query_params.get('city')
        # district = self.request.query_params.get('district')
        # if district:
        #     data = get_list_ward_of_district(city=city, district=district)
        #     print(data)
        #     ward = []
        #     total_ads = query_total.count()
        #     total_district_ads = model.count()
        #     for i in data:
        #         # if 'ward' in i:
        #         values = model.filter(split_ward=i["ward"]).count()
        #         lat_lon = None
        #         if 'lat_lon' in i.keys():
        #             lat_lon = i['lat_lon'][0]
        #         # if ('lat' and 'lon') in i.keys():
        #         #     lat, lon = i['lat'], i['lon']
        #         #### total ads perdistrict #####
        #         ward.append({
        #             'id': i['id'],
        #             'name': i['ward'],
        #             'values': values,
        #             'coordinates': lat_lon
        #         })

        #     return Response(data={
        #         'total_ads': total_ads,
        #         'total_district_ads': total_district_ads,
        #         'ads_per_ward': ward,
        #         'params': self.get_params(),
        #     })
        # else:
        data, data_map = get_data_vs_map_district_of_city(city)
        district = []
        total_ads = query_total.count()
        total_ads_of_city = model.count()
        for i in data:
            values = model.filter(split_district=i["district"]).count()
            # append data of district in to dict district
            district.append({
                'id': i['id'],
                'name': i['district'],
                'values': values,
                'name_map': i['name_map']
            })
        return Response(data={
            'total_ads': total_ads,
            'total_city_ads': total_ads_of_city,
            'ads_per_district': district,
            'data_map': data_map,
            'params': self.get_params(),
        })


class DataForExportViewSet(viewsets.ViewSet):
    def get_params(self):
        data = self.request.query_params
        params = data
        # city = data.get('city')
        # district = data.get('district')
        # ward = data.get('ward')
        # street = data.get('street') 
        # from_date = data.get('from_date')
        # to_date = data.get('to_date')
        # params = {}
        # if city:
        #     params.update({'city': city})
        # if district:
        #     params.update({'district': district})
        # if ward:
        #     params.update({'ward': ward})
        # if street:
        #     params.update({'street': street})
        # if from_date:
        #     params.update({'from_date': from_date})
        # if to_date:
        #     params.update({'to_date': to_date})
        return params

    def get_queryset(self):
        data = self.request.query_params
        # validate params
        serializer = ReportParamsValidateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # params
        year = get_year_query_drf(data.get('year'))
        city = data.get('city')
        district = data.get('district')
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        if year == 2022:
            query = query_total = RealEstate2022.objects.all()
        # elif year == 2021:
        #     query_total = RealEstate2021.objects.all()
        #     query = RealEstate2021.objects.all()
        else:
            query = query_total = RealEstate2022.objects.all()

        if city:
            query = query.filter(split_city=city)
        if self.action not in ['price_per_district', 'district_of_interest']:
            if district:
                query = query.filter(split_district=district)
        if from_date:
            query = query.filter(ads_date__gte=from_date)
        if to_date:
            query = query.filter(ads_date__lte=to_date)

        return query, query_total

    @action(methods=['post'], detail=False, url_path='data-for-exports')
    def data_for_exports(self, request):
        pass


class RealEstate2022ViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = RealEstate2022Serializer
    pagination_class = RealEstate2022Paginator
    queryset = RealEstate2022.objects.all()

    def get_queryset(self):
        query = RealEstate2022.objects.all()
        data = self.request.query_params
        # validate data params
        serialzier = ReportParamsValidateExportSerializer(data=data)
        serialzier.is_valid(raise_exception=True)
        # params
        city = data.get('city')
        district = data.get('district')
        ward = data.get('ward')
        street = data.get('street')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        # filter query
        if city:
            query = query.filter(split_city=city)
        if district:
            query = query.filter(split_district=district)
        if ward:
            query = query.filter(split_ward=ward)
        if street:
            query = query.filter(format_street=street)
        if from_date:
            query = query.filter(ads_date__gte=from_date)
        if to_date:
            query = query.filter(ads_date__lte=to_date)
        return query


# if from_month:
        #     from_month, to_month = get_month_params_for_query(
        #         data.get('from_month'), data.get('to_month'))
        #     query = query.filter(ads_date__month__gte=from_month).filter(
        #         ads_date__month__lte=to_month)
# if data.get('from_month'):
#             from_month, to_month = get_month_params_for_query(
#                 data.get('from_month'), data.get('to_month'))
#             print(from_month, to_month)
#             if from_month:
#                 query = query.filter(ads_date__month__gte=from_month).filter(
#                     ads_date__month__lte=to_month)
