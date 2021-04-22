from django.urls import path

from main.views import CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view()),
]