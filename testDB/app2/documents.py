from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

from app2.models import DetaiReport

@registry.register_document
class ReportDocument(Document):
    class Index:
        name = 'report'
        settings = {'number_of_shards': 5,
                    'number_of_replicas': 3}
    class Django:
        model = DetaiReport
        fields = ['title','price','quantity']