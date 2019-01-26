from rest_framework import serializers
from .models import Reservation, DogItems
from customer.models import Walker

class CheckSlotSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    duration = serializers.DurationField()
    walker_id = serializers.IntegerField()

    def checkslot(self, ):
        date = self.validated_data['date']
        duration = self.validated_data['date']
        walker = Walker.objects.get(id = self.validated_data['id'])
        slots = walker.slots(date, duration)
        return(slots)

class ReservationItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = DogItems
        fields = ('id' ,'reservation', 'dog')


class ReservationItemCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = DogItems
        fields = ('reservation', 'dog')


class ReservationSerializer(serializers.ModelSerializer):
    dogs = ReservationItemSerializer(many=True)
    class Meta:
        model = Reservation
        fields = ('walker', 'owner', 'date', 'duration', 'dogs', 'status', 'reward')