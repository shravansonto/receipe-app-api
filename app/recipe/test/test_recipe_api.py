from decimal import Decimal
from django.contrib.auth import get_user_model

from django.urls import reverse

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL=reverse('recipe:recipe-list')

def create_recipe(user, **params):

    default = {
        'title': 'Sample Recipe title',
        'time_minutes': 22, 
        'price': Decimal('5.25'),
        'description': 'Sample Description',
        'link': 'http://example.com/reciepe.pdf',
    }

    default.update(params)
    recipe = Recipe.objects.create(user=user, **default)
    return recipe

class PublicRecipeApiTest(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_auth_required(self):

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):

        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializers = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializers.data)

    def test_recipe_list_limited_to_user(self):

        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'passwrod123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user = self.user)
        serializers = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializers.data)


