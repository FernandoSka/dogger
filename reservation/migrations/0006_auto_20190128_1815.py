# Generated by Django 2.1.5 on 2019-01-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20190128_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('unclosed', 'unclosed'), ('pending', 'pending'), ('acepted', 'acepted'), ('concluded', 'concluded'), ('refused', 'refused'), ('canceled', 'canceled')], default='unclosed', max_length=9),
        ),
    ]
