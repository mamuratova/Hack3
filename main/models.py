from django.db import models
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=55, primary_key=True)
    name = models.CharField(max_length=55, unique=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('slug', )

    def __str__(self):
        if self.parent:
            return f'{self.parent} --> {self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False


class Product(models.Model):
    CHOICES = (
        ('in stock', 'В наличии'),
        ('out of stock', 'Нет в наличии')
    )
    Choices = (
        ('pill', 'Таблетка'),
        ('capsule', 'Капсула'),
        ('ointment', 'Мазь'),
        ('solution', 'Раствор'),
        ('syrup', 'Сироп')
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    country = models.CharField(max_length=100, default='Kyrgyzstan')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=100, choices=CHOICES)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='products')
    form = models.CharField(max_length=100, choices=Choices)
    maker = models.CharField(max_length=200, default='Dinara')
    image = models.ImageField(upload_to='products', default='default.png')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id', )


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created', )


class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


# class Rating(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
#     movie = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
#     rating = models.PositiveSmallIntegerField(default=0)


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ('product', )


# class History(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='histories')
#     movie = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='histories')
#     created = models.DateTimeField(auto_now_add=True, blank=True)

