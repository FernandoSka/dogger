# Generated by Django 2.1.5 on 2019-01-24 09:34

import customer.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20190124_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='walker',
            name='founds',
            field=models.FloatField(default=0, validators=[customer.validators.min_validator]),
        ),
        migrations.AlterField(
            model_name='walker',
            name='walks',
            field=models.IntegerField(default=0, validators=[customer.validators.min_validator]),
        ),
    ]