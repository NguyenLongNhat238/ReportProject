from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from report.models import RealEstate2022, RealEstate2021


@registry.register_document
class RealEstate2022Document(Document):
    def get_queryset(self):
        return self.django.model._default_manager.all()[0:1000]
    class Index:
        name = 'real-estate-2022'
        settings = {'number_of_shards': 12,
                    'number_of_replicas': 1}

    class Django:
        model = RealEstate2022
        fields = ['id_client', 'ads_link', 'ads_title', 'for_sale', 'for_lease',
                  'price', 'surface', 'pro_width', 'pro_length', 
                  'full_address','format_street','split_ward','split_district','split_city'
                  ]


@registry.register_document
class RealEstate2021Document(Document):
    def get_queryset(self):
        return self.django.model._default_manager.all()[0:1000]
    class Index:
        name = 'real-estate-2021'
        settings = {'number_of_shards': 12,
                    'number_of_replicas': 1}

    class Django:
        model = RealEstate2021
        fields = ['id_client', 'ads_link', 'ads_title', 'for_sale', 'for_lease',
                  'price', 'surface', 'pro_width', 'pro_length', 
                  'full_address','format_street','split_ward','split_district','split_city'
                  ]