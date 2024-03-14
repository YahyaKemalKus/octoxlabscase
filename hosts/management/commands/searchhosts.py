import json
import logging
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
import requests
from octoxlabscase import settings


class Command(BaseCommand):
    help = "Interacts with an API endpoint"

    def add_arguments(self, parser):
        parser.add_argument("--username", "-u", type=str, required=True)
        parser.add_argument("--password", "-p", type=str, required=True)
        parser.add_argument("--query", "-q", type=str, required=True)
        parser.add_argument("--port", type=int, required=False)

    def handle(self, *args, **options):
        base_url = settings.BASE_URL
        port = options["port"]
        if port:
            parsed_url = urlparse(base_url)
            base_url = parsed_url._replace(netloc=f"{parsed_url.hostname}:{port}").geturl()
        auth_endpoint = base_url + "/api/auth"
        search_endpoint = base_url + "/api/search"

        query = options["query"]
        username = options["username"]
        password = options["password"]

        session = requests.Session()
        auth_request = session.post(auth_endpoint, json={"username": username,
                                                         "password": password})
        api_key = auth_request.json()["data"]["token"]
        session.headers.update({"Authorization": api_key})

        data = {
            "query": query
        }
        try:
            response = session.post(search_endpoint, json=data)
            prettified_response = json.dumps(response.json(), indent=4)
            self.stdout.write(prettified_response)
        except requests.RequestException as e:
            self.stdout.write(f"Error: {e}")
