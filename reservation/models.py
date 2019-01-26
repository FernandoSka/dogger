from django.db import models
from customer.models import Walker, Owner, Dog
from customer.validators import min_validator, rate_validator

class Reservation(models.Model):
	CHOICES = (
		('unclosed', 'unclosed'),
		('pending', 'pending'),
		('acepted', 'acepted'),
		('concluded', 'concluded'),
		('refused', 'refused'),
		('canceled', 'canceled'),

	)
	walker = models.ForeignKey(Walker, on_delete = models.CASCADE)
	owner = models.ForeignKey(Owner, on_delete = models.CASCADE)
	date = models.DateTimeField()#add validator
	duration  = models.DurationField()#add validator
	dogs = models.ManyToManyField(Dog, through = 'DogItems')
	status = models.CharField(max_length = 9, choices=CHOICES, default='pending')
	reward = models.FloatField(validators = [min_validator])
	rate = models.IntegerField(validators = [rate_validator], default=5)

class DogItems(models.Model):
	reservation = models.ForeignKey(Reservation, on_delete = models.CASCADE, related_name='dog_item')
	dog = models.ForeignKey(Dog, on_delete = models.CASCADE, related_name = 'reservation_item')
	