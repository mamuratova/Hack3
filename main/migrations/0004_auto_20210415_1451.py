# Generated by Django 3.1 on 2021-04-15 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210415_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='expiration_date1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='expiration_date2',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.png', upload_to='products'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
