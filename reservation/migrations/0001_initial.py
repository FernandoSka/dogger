# Generated by Django 2.1.5 on 2019-01-24 07:21

import customer.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Dog')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('acepted', 'acepted'), ('concluded', 'concluded'), ('refused', 'refused'), ('canceled', 'canceled')], default='pending', max_length=9)),
                ('reward', models.FloatField(validators=[customer.validators.min_validator])),
                ('dogs', models.ManyToManyField(through='reservation.DogItems', to='customer.Dog')),
                ('walker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Walker')),
            ],
        ),
        migrations.AddField(
            model_name='dogitems',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.Reservation'),
        ),
    ]
