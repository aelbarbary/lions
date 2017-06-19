from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts =[ '192.168.99.100'], port= 32771)

class ResourceIndex(DocType):
    Name = Text()
    created_date = Date()
    description = Text()
    link = Text()
    image = Text()
    class Meta:
        index = 'avacat'

def bulk_indexing():
    ResourceIndex.init()
    es = Elasticsearch([
        {'host': '192.168.99.100', 'port': 32771}
    ])
    bulk(client=es, actions=(b.indexing() for b in models.Resource.objects.all().iterator()))
