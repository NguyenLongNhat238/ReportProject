from rest_framework import serializers
from django.conf import settings
from .models import RealEstate2021


class RealEstate2021Serializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate2021
        fields = ['id', 'id_client', 'ads_link', 'ads_title', 'ads_date', 'for_sale', 'for_lease', 'land_type',
                  'price', 'price_m2', 'surface', 'pro_width', 'pro_length',
                  'full_address', 'format_street', 'split_ward', 'split_district', 'split_city',
                  'dealer_email', 'dealer_tel', 'dealer_name'
                  ]
