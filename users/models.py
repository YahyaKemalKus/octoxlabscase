import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class OctoXLabsUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
