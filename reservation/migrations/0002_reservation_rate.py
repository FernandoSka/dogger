# Generated by Django 2.1.5 on 2019-01-24 09:56

import customer.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='rate',
            field=models.IntegerField(default=5, validators=[customer.validators.rate_validator]),
        ),
    ]
