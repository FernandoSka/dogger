# Generated by Django 2.1.5 on 2019-01-24 07:37

import customer.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='walker',
            name='rate',
        ),
        migrations.AddField(
            model_name='customer',
            name='rate',
            field=models.IntegerField(default=5, validators=[customer.validators.rate_validator]),
            preserve_default=False,
        ),
    ]