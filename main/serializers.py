from django.db.models import Avg
from rest_framework.decorators import action

from .models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created = serializers.DateTimeField(format='%d %B %Y %H:%M', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        problem = Product.objects.create(**validated_data)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = len(LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data)
        pr = Product.objects.filter(category=instance.category.slug)
        comment = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product', 'user', 'like')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('user')
            fields.pop('like')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data.get('product')
        like = Like.objects.get_or_create(user=user, product=product)[0]
        like.like = True if like.like is False else False
        like.save()
        return like


class ParsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    photo = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=100)
    link = serializers.CharField(max_length=300)


# class FavoriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ('id', 'movie', 'user', 'favorite')
#
#     def get_fields(self):
#         action = self.context.get('action')
#         fields = super().get_fields()
#         if action == 'create':
#             fields.pop('user')
#             fields.pop('favorite')
#         return fields
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         movie = validated_data.get('movie')
#         favorite = Favorite.objects.get_or_create(user=user, movie=movie)[0]
#         favorite.favorite = True if favorite.favorite == False else False
#         favorite.save()
#         return favorite
#
#
# class RatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rating
#         fields = ('movie', 'user', 'rating')
#
#     def validate(self, attrs):
#         rating = attrs.get('rating')
#         if rating > 5:
#             raise serializers.ValidationError('The value must not exceed 5')
#         return attrs
#
#     def get_fields(self):
#         fields = super().get_fields()
#         action = self.context.get('action')
#         if action == 'create':
#             fields.pop('user')
#         return fields
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         movie = validated_data.get('movie')
#         rat = validated_data.get('rating')
#         rating = Rating.objects.get_or_create(user=user, movie=movie)[0]
#         rating.rating = rat
#         rating.save()
#         return rating


















# class CartSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = ('quantity', 'dessert')
#     dessert = DessertSerializer()
#
#
# class CartItemSerializer(serializers.Serializer):
#     dessert_id = serializers.IntegerField(required=True, write_only=True)
#     quantity = serializers.IntegerField(default=1)
#     dessert = DessertSerializer(read_only=True)
#
#
# class CartItemsSerializer(serializers.Serializer):
#     desserts = serializers.ListField(child=CartItemSerializer())
#
#     def create(self, validated_data):
#         """Add desserts to cart."""
#         # Get current user
#         user = self.context['request'].user
#
#         # Get current car items
#         current_cart = CartItem.objects.filter(owner=user)
#         current_cart_items_ids = map(lambda item: item.dessert_id, current_cart)
#
#         # List to prepare items in-memory for bulk save
#         cart_items = list()
#
#         for dessert_data in validated_data['desserts']:
#             dessert_id = dessert_data['dessert_id']
#             # Break and return 400 if a dessert already in cart
#             if dessert_id in current_cart_items_ids:
#                 raise exceptions.ParseError(detail="Dessert (%s) alraedy exists in the cart" % dessert_id)
#                 return
#             try:  # Check if item_id added to cart is valid dessert_id else return 400
#                 dessert = Dessert.objects.get(id=dessert_id)  # FIXME: Bulk query instead of looping
#             except Dessert.DoesNotExist:
#                 raise exceptions.ParseError(detail="No such Dessert ID (%s)" % dessert_id)
#                 return
#
#             # Create CartItem in memory and add to cart_items list
#             quantity = dessert_data['quantity']
#             cart_items.append(
#                 CartItem(owner=user, dessert=dessert, quantity=quantity)
#             )
#
#         # Bulk save cart_items to DB
#         result = CartItem.objects.bulk_create(cart_items)
#
#         # Merge recently added items with the current ones in 'shared_with'cart to resturn
#         # response with all items in cart
#         response = {'desserts': list(current_cart) + result}
#         return response
#
#
# class OrderDessertSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = OrderDessert
#         fields = ('quantity', 'dessert')
#
#     dessert = DessertSerializer(many=False, read_only=True)
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ('id', 'created_at', 'url', 'orderdessert_set',)
#
#     orderdessert_set = OrderDessertSerializer(many=True, read_only=True)
#
#
# class WishlistSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Wishlist
#         fields = ('id', 'url', 'name', 'owner', 'desserts', 'shared_with',)





