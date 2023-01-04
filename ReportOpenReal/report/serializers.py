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
    ads_year = serializers.IntegerField(required=False, default=2022)

    # def is_valid(self, *, raise_exception=False):
    #     assert hasattr(self, 'initial_data'), (
    #         'Cannot call `.is_valid()` as no `data=` keyword argument was '
    #         'passed when instantiating the serializer instance.'
    #     )

    #     if not hasattr(self, '_validated_data'):
    #         try:
    #             self._validated_data = self.run_validation(self.initial_data)
    #         except exceptions.ValidationError as exc:
    #             self._validated_data = {}
    #             self._errors = exc.detail
    #         else:
    #             self._errors = {}
    #     try:
    #         if self._validated_data['from_date'] > self._validated_data['to_date']:
    #             self._errors.update({
    #                 'from_date and to_date': 'from_date must be small than to_date'
    #             })

    #         if self._validated_data['to_date'] > date.today():
    #             self._errors.update({
    #                 'to_date ': 'to_date must be small than now date'
    #             })
    #     except:
    #         pass

    #     if (self.to_date - self.from_date) > MAX_MONTH_QUERY_REPORTS*30:
    #         self._errors.append({
    #             'from_date and to_date': 'from_date must be small than to_date'
    #         })

    #     if self._errors and raise_exception:
    #         raise exceptions.ValidationError(self.errors)

    #     return not bool(self._errors)

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

        # if error:
        #     raise serializers.ValidationError({'error': 'aa'})
        return super().validate(data)
