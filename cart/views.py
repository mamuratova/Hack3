from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Product

from .models import Cart, CartItem
from .serializers import CartSerializer


class CartAPIView(APIView, DestroyModelMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_obj, _ = Cart.objects.get_existing_or_new(request)
        context = {'request': request}
        serializer = CartSerializer(cart_obj, context=context)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get("quantity", 1))
        product_obj = get_object_or_404(Product, pk=product_id)
        cart_obj, _ = Cart.objects.get_existing_or_new(request)

        if quantity <= 0:
            cart_item_qs = CartItem.objects.filter(
                cart=cart_obj, product=product_obj)
            if cart_item_qs.count != 0:
                cart_item_qs.first().delete()
        else:
            cart_item_obj, created = CartItem.objects.get_or_create(
                product=product_obj, cart=cart_obj)
            cart_item_obj.quantity = quantity
            cart_item_obj.save()

        serializer = CartSerializer(cart_obj, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        CartItem.objects.all().delete()
        return Response('Successfully clear list!', status=status.HTTP_200_OK)


class CheckProductInCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product_id = int(request.data.get('product'))
        product_obj = get_object_or_404(Product, id=product_id)
        cart_obj, created = Cart.objects.get_existing_or_new(request)
        return Response(not created and CartItem.objects.filter(cart=cart_obj, product=product_obj).exists())

    def delete(self, request, *args, **kwargs):
        product = Product.objects.get(id=int(request.data.get('product')))
        CartItem.objects.get(product=product.id).delete()
        return Response('Successfully delete!', status=status.HTTP_200_OK)


