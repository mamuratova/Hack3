from django.db.models import Q
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import *
from .parsing import pars
from .permissions import IsCommentAuthor


class MyPaginationClass(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        for i in range(self.page_size):
            text = data[i]['description']
            data[i]['description'] = text[:15] + '...'
            likes = data[i]['likes']
            data[i]['likes'] = len(likes)
            comments = data[i]['comments']
            data[i]['comments'] = len(comments)
        return super().get_paginated_response(data)


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminUser, ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsAdminUser, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PermissionForComment:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permissions = [IsCommentAuthor, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProductViewSet(PermissionMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MyPaginationClass

    @action(methods=['GET'], detail=False)
    def search(self, request):
        query = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'A-Z':
            queryset = self.get_queryset().order_by('name')
        elif filter == 'Z-A':
            queryset = self.get_queryset().order_by('-name')
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(PermissionForComment, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class FavoriteListView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        query = self.request.user
        queryset = Favorite.objects.filter(user=query, favorite=True)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class ParsOcView(APIView):
    def get(self, request):
        dict_ = pars()
        serializer = ParsSerializer(instance=dict_, many=True)
        return Response(serializer.data)



# class RatingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_serializer_context(self):
#         return {'request': self.request, 'action': self.action}



