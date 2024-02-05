from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal 

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):

        email = 'test@example.com'
        password = 'testpass@123'
        user = get_user_model().objects.create_user(
                email=email, 
                password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):

        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['Test3@EXAMPLE.COM', 'Test3@example.com']
        ]

        for email, expected_email in sample_emails:

            user = get_user_model().objects.create_user(email=email)
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser('test5@example.com', 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):

        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
        )
        recipe = models.Recipe.objects.create(
            user = user, 
            title = 'Simple recipe name',
            time_minutes = 5,
            price=Decimal('5.50'),
            description = 'Sample reciepe description',
        )

        self.assertEqual(str(recipe), recipe.title)
    