from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token

from authentication.models import User


class GenericTestCase(TestCase):
    fixtures = []
    email = "test@test.com"
    password = "12345"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.token = Token.objects.create(user=self.user)

    def get_request(self, endpoint):
        request = self.factory.get(endpoint)
        request.META["HTTP_AUTHORIZATION"] = f"Token {self.token.key}"
        request.user = self.user
        return request

    def post_request(self, endpoint, data=None):
        if data:
            request = self.factory.post(endpoint, data, format="json")
        else:
            request = self.factory.post(endpoint)

        request.META["HTTP_AUTHORIZATION"] = f"Token {self.token.key}"
        request.user = self.user
        return request

    def put_request(self, endpoint, data=None):
        if data:
            request = self.factory.put(endpoint, data, format="json")
        else:
            request = self.factory.put(endpoint)

        request.META["HTTP_AUTHORIZATION"] = f"Token {self.token.key}"
        request.user = self.user
        return request
