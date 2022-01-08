from django.http import Http404

from .serializers import ProductSerializer
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from.models import Product


class LastestProductsList(APIView):

    def get(self, request, format=None):
        # get first 4 products from db
        products = Product.objects.all()[0:4]
        # convert db response using serializer (more than one product returned so we use many=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
