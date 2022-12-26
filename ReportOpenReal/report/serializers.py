from rest_framework import serializers
from django.conf import settings
from .models import RealEstate2021, RealEstate2022


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

        # def to_representation(self, obj):
        #     primitive_repr = super(RealEstate2022Serializer, self).to_representation(obj)
        #     primitive_repr['The Author'] = primitive_repr['author_name']

        #     return primitive_repr