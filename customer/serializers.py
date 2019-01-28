from django.contrib.auth.models import User
from .models import Customer, Walker, Owner, Dog
from rest_framework import serializers
from .validators import required

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self):
        return User(**self.validated_data)

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    class Meta:
        model = Customer
        fields = ('user', 'country', 'city', 'address', 'image')

    def create(self):
        return Customer(**self.validated_data)

class WalkerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)

    class Meta:
        model = Walker
        fields = ('customer', 'walks', 'founds', 'pending_reservations')

    def create(self):
        return Walker(**self.validated_data)

class OwnerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)

    class Meta:
        model = Owner
        fields = ('customer', 'reservations', 'id')

class UserSerializerEdit(serializers.ModelSerializer):
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class WalkerDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)

    class Meta:
        model = Walker
        fields = ('customer', 'walks', 'id')

    def create(self):
        return Walker(**self.validated_data)


class DogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Dog
        fields = ('id', 'name', 'race', 'age','image', 'comments')

    def create(self):
        return Dog(**self.validated_data)

class DogSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Dog
        fields = ('name', 'race', 'age','image', 'comments')

    def create(self):
        return Dog(**self.validated_data)