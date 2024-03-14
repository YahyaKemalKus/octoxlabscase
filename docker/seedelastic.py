import logging
import os
from time import sleep

import elastic_transport
import elasticsearch

if __name__ == '__main__':
    env = os.environ
    index = env.get("ELASTIC_INDEX")
    while True:
        try:
            client = elasticsearch.Elasticsearch(
                hosts=env.get("ELASTIC_HOST"),
                basic_auth=(env.get("ELASTIC_USERNAME"), env.get("ELASTIC_PASSWORD")),
                verify_certs=False)
            if not client.indices.exists(index=index):
                client.index(index=index, body={})
                client.indices.put_mapping(index=index, body={
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
                })

                client.index(index=index, id="d8d0764f-96ee-42a3-adff-3364dd6cb386", body={
                    "hosts": [{"Hostname": "octoxlabs01", "Ip": "0.0.0.0"}]
                })
                client.index(index=index, id="f544837b-7b8e-44a3-81bb-7ff581008100", body={
                    "hosts": [{"Hostname": "irrelevant", "Ip": "0.0.0.0"}]
                })

                client.indices.refresh(index=index)
            break
        except (elastic_transport.ConnectionError, elasticsearch.AuthenticationException):
            logging.warning("Could not connect to Elasticsearch, retrying in 1 second")
            sleep(1)
