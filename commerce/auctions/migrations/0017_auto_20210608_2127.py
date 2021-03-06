# Generated by Django 3.1.7 on 2021-06-08 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210608_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='winner',
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentItems', to='auctions.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidItems', to='auctions.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='comments',
            field=models.ManyToManyField(blank=True, default='', related_name='comments', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='product',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchers', to=settings.AUTH_USER_MODEL),
        ),
    ]
