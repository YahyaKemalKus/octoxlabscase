from typing import Dict, List, TypedDict

from dependency_injector.wiring import inject, Provide
from elasticsearch import Elasticsearch
from pydantic import BaseModel, StrictStr
from common.exceptions import ApplicationError
from octoxlabscase import HostsContainer


class HostModel(BaseModel):
    Hostname: StrictStr
    Ip: StrictStr

    class HostDict(TypedDict):
        Hostname: str
        Ip: str

    @classmethod
    def from_list(cls, hosts: List[HostDict]) -> 'List[HostModel]':
        return [cls(**host) for host in hosts]


class HostESModel(BaseModel):
    id: StrictStr
    hosts: List[HostModel]

    @classmethod
    def from_list_of_hits(cls, hits: List) -> 'List[HostESModel]':
        results = list()
        for hit in hits:
            results.append(cls(id=hit["_id"], hosts=HostModel.from_list(hit["_source"]["hosts"])))
        return results


@inject
def search_hosts(
        *,
        query: str,
        es_client: Elasticsearch = Provide[HostsContainer.es_client],
        es_index: str = Provide[HostsContainer.es_index]
) -> List[HostESModel]:
    es_query = convert_str_to_elasticsearch_query(query=query)
    results = es_client.search(
        index=es_index,
        query=es_query
    )["hits"]["hits"]
    return HostESModel.from_list_of_hits(results)


def convert_str_to_elasticsearch_query(
        *,
        query: str
) -> Dict:
    try:
        key, value = query.split(' = ')
    except (ValueError, AttributeError):
        raise ApplicationError(message="Invalid query")
    elasticsearch_query = {
        "nested": {
            "path": "hosts",
            "query": {
                "wildcard": {
                    f"hosts.{key}": {
                        "value": value
                    }
                }
            }
        }
    }

    return elasticsearch_query
