from dependency_injector import containers, providers
from elasticsearch import Elasticsearch

from octoxlabscase import settings


class HostsContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    es_client = providers.Factory(
        Elasticsearch,
        hosts=config.ELASTIC_HOST,
        basic_auth=providers.List(config.ELASTIC_USERNAME, config.ELASTIC_PASSWORD),
        verify_certs=False
    )
    es_index = providers.Object(settings.ELASTIC_INDEX)
