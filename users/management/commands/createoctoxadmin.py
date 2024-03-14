import logging

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Creates a new super user'
    USER_MODEL = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument('--password', "-p", type=str, required=True)
        parser.add_argument('--username', "-u", type=str, required=True)
        parser.add_argument('--email', "-e", type=str, required=True)

    def handle(self, *args, **options):
        password = options['password']
        username = options['username']
        email = options['email']
        try:
            self.USER_MODEL.objects.create_superuser(username=username, password=password, email=email)
            logging.info("Successfully created")
        except IntegrityError:
            logging.warning("User already exists")
