# Generated by Django 3.1.7 on 2021-05-30 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210527_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='product',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchers', to=settings.AUTH_USER_MODEL),
        ),
    ]
