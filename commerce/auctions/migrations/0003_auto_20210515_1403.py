# Generated by Django 3.1.7 on 2021-05-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210515_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.FloatField(),
        ),
    ]
