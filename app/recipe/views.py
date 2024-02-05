from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = RecipeSerializer

    queryset = Recipe.objects.all()

    authenticated_classes = [TokenAuthentication]

    permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
