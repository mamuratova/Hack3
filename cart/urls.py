from django.urls import path

from .views import *

urlpatterns = [
    path('', CartAPIView.as_view()),
    path('item/', CheckProductInCart.as_view()),
]
