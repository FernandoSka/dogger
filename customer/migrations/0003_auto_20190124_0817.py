# Generated by Django 2.1.5 on 2019-01-24 08:17

import customer.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190124_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(null=True, upload_to='customer-images', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='rate',
            field=models.IntegerField(default=5, validators=[customer.validators.rate_validator]),
        ),
    ]
