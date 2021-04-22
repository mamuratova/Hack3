from django.contrib import admin
from django.contrib.admin import ModelAdmin
from main.models import *


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Like)

