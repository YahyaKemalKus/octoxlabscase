import pytest
from django.test import TestCase
from elasticsearch import Elasticsearch

from common.exceptions import ApplicationError
from octoxlabscase import hosts_container
from hosts import selectors
from octoxlabscase.settings import ELASTIC_TEST_INDEX, ELASTIC_TEST_HOST


class TestHostsSelectors(TestCase):
    """
    **Many more advanced tests can be implemented with factories and faker**.
    """

    @classmethod
    def setUpClass(cls):
        cls.es = Elasticsearch(ELASTIC_TEST_HOST)
        body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
            },
            "mappings": {
                "properties": {
                    "hosts": {
                        "type": "nested",
                        "properties": {
                            "Hostname": {
                                "type": "text"
                            },
                            "Ip": {
                                "type": "text"
                            }
                        }
                    }
                }
            },
        }

        cls.es.indices.create(index=ELASTIC_TEST_INDEX, body=body)

        test_data = [
            {
                "hosts": [{"Hostname": "octoxlabs01", "Ip": "0.0.0.0"}]
            },
            {
                "hosts": [{"Hostname": "host_with_no_ip"}]
            },
            {
                "hosts": [{"Hostname": "oCtOxLabs", "Ip": "0.0.0.0"}]
            },
            {
                "hosts": [{"Hostname": "00octoxlabs00", "Ip": "0.0.0.0"}]
            },
            {
                "hosts": [{"Hostname": "irrelevant", "Ip": "0.0.0.0"}]
            }
        ]
        for test_datum in test_data:
            cls.index_test_fixtures(
                es=cls.es,
                index_name=ELASTIC_TEST_INDEX,
                data=test_datum,
            )

    @classmethod
    def tearDownClass(cls):
        indices = cls.es.indices.get(index="*")
        for index_name in indices:
            cls.es.indices.delete(index=index_name)

    @staticmethod
    def index_test_fixtures(es, index_name, data):
        created = es.index(index=index_name, body=data)
        assert created["result"] == "created"
        es.indices.refresh(index=index_name)

    def test_search_hosts_with_valid_query(self):
        # can be overriden with a mock class
        with hosts_container.es_client.override(self.es), \
                hosts_container.es_index.override(ELASTIC_TEST_INDEX):
            results = selectors.search_hosts(query="Hostname = octoxlabs*")
            assert isinstance(results, list)
            assert len(results) == 2
            for result in results:
                assert isinstance(result, selectors.HostESModel)
                assert isinstance(result.hosts, list)
                assert isinstance(result.id, str)
                for host in result.hosts:
                    assert host.Hostname is not None
                    assert host.Hostname.lower().startswith("octoxlabs")

    def test_search_hosts_with_invalid_query(self):
        # invalid queries can be extended
        invalid_queries = [
            "Hostname= octoxlabs*",
            "Hostname =octoxlabs*",
            "Hostname=octoxlabs*",
            "Hostname = octoxlabs = *",
            "hello world",
        ]
        with hosts_container.es_client.override(self.es), \
                hosts_container.es_index.override(ELASTIC_TEST_INDEX):
            for query in invalid_queries:
                with pytest.raises((ValueError, ApplicationError)):
                    selectors.search_hosts(query=query)
