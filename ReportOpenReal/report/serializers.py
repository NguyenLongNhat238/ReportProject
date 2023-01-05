from rest_framework import serializers
from django.conf import settings
from dateutil.parser import parse
from constant.config import MAX_MONTH_QUERY_REPORTS
from .models import RealEstate2021, RealEstate2022
from rest_framework import exceptions
from datetime import datetime, date, timedelta


class RealEstate2021Serializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate2021
        fields = ['id', 'id_client', 'ads_link', 'ads_title', 'ads_date', 'for_sale', 'for_lease', 'land_type',
                  'price', 'price_m2', 'surface', 'pro_width', 'pro_length',
                  'full_address', 'format_street', 'split_ward', 'split_district', 'split_city',
                  'dealer_email', 'dealer_tel', 'dealer_name'
                  ]


class RealEstate2022Serializer(serializers.ModelSerializer):
    class Meta:

        model = RealEstate2022
        fields = ['land_type', 'ads_date', 'price', 'price_m2', 'surface',
                  'used_surface', 'pro_width', 'pro_length', 'legal_status', 'pro_current_status', 'pro_direction',
                  'frontage', 'alley_access', 'pro_utilities', 'nb_rooms', 'nb_floors', 'full_address', 'format_hs', 'format_street',
                  'split_ward', 'split_district', 'split_city', 'lat', 'lon', 'ads_title', 'detailed_brief',
                  'dealer_name', 'dealer_address', 'dealer_email', 'dealer_type', 'dealer_tel',
                  'project_name', 'agency_name', 'agency_address', 'agency_city', 'agency_tel', 'agency_website']


class ReportParamsValidateSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=True)
    to_date = serializers.DateField(required=True)
    city = serializers.CharField(required=True)
    district = serializers.CharField(required=True)
    ward = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    ads_year = serializers.IntegerField(required=False, default=2022)

    def validate(self, data):
        from_date = data['from_date']
        to_date = data['to_date']
        error = []
        if from_date > to_date:
            raise serializers.ValidationError({'error': 'Ngày bắt đầu phải nhỏ hơn ngày kết thúc.'
                                               })
        if to_date > date.today():
            raise serializers.ValidationError({'error': 'Ngày kết thúc phải không được quá ngày hôm nay.'
                                               })
        if (to_date - from_date) > timedelta(days=MAX_MONTH_QUERY_REPORTS*30):
            raise serializers.ValidationError({'error': f'Bạn chỉ có thể xem báo cáo trong vòng {MAX_MONTH_QUERY_REPORTS} tháng.'
                                               })

        return super().validate(data)


class ReportParamsValidateExportSerializer(ReportParamsValidateSerializer):
    ward = serializers.CharField(required=True)
    street = serializers.CharField(required=True)