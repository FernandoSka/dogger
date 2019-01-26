from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    CustomerSerializer,
    WalkerSerializer,
    OwnerSerializer,
    WalkerDetailSerializer,
    UserSerializerEdit,
    DogSerializer,
    DogSerializerCreate
)
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Customer, Walker, Owner, Dog
from rest_framework.permissions import IsAuthenticated


class CreateWalker(APIView):        

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        customer_serializer = CustomerSerializer(data = request.data)
        if user_serializer.is_valid():
            if customer_serializer.is_valid():
                user = user_serializer.create()
                user.set_password(user_serializer.validated_data['password'])
                user.save()
                customer = customer_serializer.create()
                customer.user=user
                customer.save()
                walker = Walker(customer = customer)
                walker.save()
                data = user_serializer.data
                data.update(customer_serializer.data)
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        customer_serializer.is_valid()
        errors = user_serializer.errors
        errors.update(customer_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOwner(APIView):

    def post(self, request, format=None):
        user_serializer = UserSerializer(data=request.data)
        customer_serializer = CustomerSerializer(data = request.data)
        if user_serializer.is_valid():
            if customer_serializer.is_valid():
                user = user_serializer.create()
                user.set_password(user_serializer.validated_data['password'])
                user.save()
                customer = customer_serializer.create()
                customer.user=user
                customer.save()
                owner = Owner(customer = customer)
                owner.save()
                data = user_serializer.data
                data.update(customer_serializer.data)
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        customer_serializer.is_valid()
        errors = user_serializer.errors
        errors.update(customer_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class WalkerDashboard(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = self.request.user
        walker_serializer = WalkerSerializer(user.customer.walker)
        return Response(walker_serializer.data)

    def put(self, request, format=None):
        user = self.request.user
        user_serializer = UserSerializerEdit(user, data=request.data)
        customer_serializer = CustomerSerializer(user.customer, data=request.data)
        if user_serializer.is_valid():
            if customer_serializer.is_valid():
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        errors = user_serializer.errors
        errors.update(customer_serializer.errors)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerDashboard(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        owner_serializer = OwnerSerializer(user.customer.owner)
        return Response(owner_serializer.data)

    def put(self, request, format=None):
        user = self.request.user
        user_serializer = UserSerializerEdit(user, data=request.data)
        customer_serializer = CustomerSerializer(user.customer, data=request.data)
        if user_serializer.is_valid():
            if customer_serializer.is_valid():
                return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        errors = user_serializer.errors
        errors.update(customer_serializer.errors)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalkerList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        customers = Customer.objects.filter(city=user.customer.city).exclude(id=user.customer.id)
        walkers = []
        for customer in customers:
            try:
                walkers.append(customer.walker)
            except Exception as e:
                pass
        walker_serializer = WalkerDetailSerializer(walkers, many=True)
        return Response(walker_serializer.data)


class OwnerDog(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format = None):
        user = self.request.user
        dogs = user.customer.owner.dogs.all()
        dog_serializer = DogSerializer(dogs, many=True)
        return Response(dog_serializer.data)

    def post(self,request, format = None):
        user = self.request.user
        dog_serializer = DogSerializerCreate(data = request.data)
        if dog_serializer.is_valid():
            dog = dog_serializer.create()
            dog.owner = user.customer.owner
            print(dog)
            dog.save()
            return Response(dog_serializer.data, status=status.HTTP_201_CREATED)
        return Response(dog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, format = None):
        user = self.request.user
        dog = Dog.objects.get(id=request.data['id'])
        dog_serializer = DogSerializer(dog, data = request.data)
        if dog.owner == user.customer.owner:
            if dog_serializer.is_valid():
                dog_serializer.save()
                return Response(dog_serializer.data, status=status.HTTP_201_CREATED)
            return Response(dog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'owner':'This dog isnt owns to you'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, format = None):
        user = self.request.user
        dog = Dog.objects.get(id=request.data['id'])
        dog_serializer = DogSerializer(dog, data = request.data)
        if dog.owner == user.customer.owner:
            if dog_serializer.is_valid():
                dog.delete()
                return Response(dog_serializer.data, status=status.HTTP_201_CREATED)
            return Response(dog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'owner':'This dog isnt owns to you'}, status=status.HTTP_400_BAD_REQUEST)

