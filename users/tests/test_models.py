from django.test import TestCase
from users.models import User


class UserTestCase(TestCase):

    def setUp(self):
        self.manager_user = User.objects.create(
            username='john@test.com',
            email='john@test.com',
            is_account_manager=True,
        )
        self.client_user = User.objects.create(
            
        )