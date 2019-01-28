from rest_framework import serializers
from .models import Reservation, DogItems
from customer.models import Walker
from customer.serializers import DogSerializer

class CheckSlotSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    duration = serializers.DurationField()
    walker_id = serializers.IntegerField()

    def checkslot(self):
        date = self.validated_data['date']
        duration = self.validated_data['date']
        walker = Walker.objects.get(id = self.validated_data['id'])
        slots = walker.slots(date, duration)
        return(slots)

class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogItems
        fields = ('reservation', 'dog')
        


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('walker', 'owner', 'date', 'duration', 'status', 'reward')

    def create(self):
        return Reservation(**self.validated_data)

class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('status',)

    def create(self):
        return Reservation(**self.validated_data)

class ReservationDetailSerializer(serializers.ModelSerializer):
    dogs = DogSerializer(many=True)
    class Meta:
        model = Reservation
        fields = ('id', 'walker', 'owner', 'date', 'duration','dogs','status', 'reward')


class ReservationEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('date', 'duration','reward')
