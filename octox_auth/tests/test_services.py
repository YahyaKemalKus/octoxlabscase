from django.contrib.auth import get_user_model
from django.test import TestCase

from octoxlabscase import settings
from octox_auth import services


class TestOctoXAuthServices(TestCase):
    USER_MODEL = get_user_model()

    @classmethod
    def setUp(cls):
        cls.USER_MODEL.objects.create_user(username='test', email='test@test.com', password='123456')
        cls.USER_MODEL.objects.create_superuser(
            username=settings.OCTOXLABS_SUPERUSER_NAME,
            email="octoxlabs@octoxlabs.com",
            password="123456"
        )

    def test_authenticate_with_octoxlabs_special_user_credentials(self):
        token = services.authenticate(username=settings.OCTOXLABS_SUPERUSER_NAME, password="123456")
        assert token
        assert isinstance(token, str)
        assert token.startswith(settings.AUTH_HEADER_PREFIX)
        assert len(token.split(" ")) == 2

    def test_authenticate_with_octoxlabs_normal_user_credentials(self):
        token = services.authenticate(username="test", password="123456")
        assert token
        assert isinstance(token, str)
        assert token.startswith("Bearer")
        assert len(token.split(" ")) == 2

    def test_authenticate_with_invalid_credentials(self):
        token = services.authenticate(username="nonexistent", password="<PASSWORD>")
        assert token is None
