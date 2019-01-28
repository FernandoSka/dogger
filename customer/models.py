from django.db import models
from django.contrib.auth.models import User
from .validators import min_validator, rate_validator

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='customer')
    country = models.CharField(max_length = 90)
    city = models.CharField(max_length = 189)
    address = models.CharField(max_length = 300)
    image = models.ImageField('image', upload_to = 'customer-images', null=True)

class Walker(models.Model):
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, related_name = 'walker')
    walks = models.IntegerField(validators = [min_validator], default = 0)
    founds = models.FloatField(validators = [min_validator], default = 0)

    def pending_reservations(self):
        from reservation.models import Reservation
        reservations = Reservation.objects.filter(walker = self, status ='pending')
        return reservations

    def slots(self, date, duration):
        date2 = date + duration
        from reservation.models import Reservation
        choices = ('pending', 'acepted')
        reservations = Reservation.objects.filter(
            walker = self,
            date__gte = date,
            date__lte = date2,
            status__in = choices
        )
        total_dogs = 0
        for reservation in reservations:
            dogs = reservation.dogs.all().count()
            if dogs > total_dogs:
                total_dogs = total_dogs
        return(3 - total_dogs)


class Owner(models.Model):
    customer = models.OneToOneField(Customer, on_delete = models.CASCADE, related_name='owner')
    reservations = models.IntegerField(validators = [min_validator], default=0)

class Dog(models.Model):
    owner = models.ForeignKey(Owner, on_delete = models.CASCADE, related_name = 'dogs')
    name = models.CharField(max_length = 150)
    race = models.CharField(max_length = 150)
    age = models.IntegerField(validators = [min_validator])
    image = models.ImageField('image', upload_to = 'dog-images', null=True, blank=True)
    comments = models.TextField(null=True,blank=True)