from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ReservationSerializer,
    CheckSlotSerializer,
    ReservationItemSerializer,
    ReservationDetailSerializer,
    ReservationEditSerializer,
    ReservationStatusSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsWalker
from .models import Reservation, DogItems
from django.utils import timezone

class ReservationCreate(APIView):
    permission_classes = (IsAuthenticated,IsOwner)
    def post(self, request, format=None):
        serializer = ReservationSerializer(data= request.data)
        if serializer.is_valid():
            reservation = serializer.create()
            slots = reservation.walker.slots(reservation.date, reservation.duration)
            if slots > 0:
                reservation.save()
                data = serializer.data
                data['id'] = reservation.id
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Reservation error': 'Can not create reservations in that time lapse'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format = None):
        try:
            reservations = Reservation.objects.filter(owner = self.request.user.customer.owner)
            res_serializer = ReservationDetailSerializer(reservations, many=True)
            return Response(res_serializer.data)
        except Exception as e:
            try:
                reservations = Reservation.objects.filter(walker = self.request.user.customer.walker).exclude(status='unclosed')
                res_serializer = ReservationDetailSerializer(reservations, many=True)
                return Response(res_serializer)
            except:
                return Response({'Customer error': 'The user has no customer'})

    def put(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.owner != self.request.user.customer.owner:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'unclosed':
            serializer = ReservationEditSerializer(reservation, data= request.data)
            if serializer.is_valid():
                slots = reservation.walker.slots(serializer.validated_data['date'], serializer.validated_data['duration'])
                if slots > 0:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'Reservation error': 'Can not create reservations in that time lapse'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.owner != self.request.user.customer.owner:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'unclosed':
            reservation.delete()
            return Response({'Object deleted': 'object deleted'}, status=status.HTTP_201_CREATED)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)


class AddDogItem(APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def post(self, request, format=None):
        item_serializer = ReservationItemSerializer(data = request.data)
        if item_serializer.is_valid():
            dog = item_serializer.validated_data['dog']
            if dog.owner != self.request.user.customer.owner:
                return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
            reservation = item_serializer.validated_data['reservation']
            if reservation.walker.slots(reservation.date, reservation.duration) - reservation.dogs.all().count() > 0:
                if item_serializer.validated_data['dog'] not in reservation.dogs.all():
                    item_serializer.save()
                return Response(item_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Reservation error': 'Can not create reservations in that time lapse'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, format = None):
        serializer = ReservationItemSerializer(data = request.data)
        if serializer.is_valid():
            reservation = serializer.validated_data['reservation']
            try:
                if reservation.owner != self.request.user.customer.owner:
                    Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
            if reservation.status == 'unclosed':
                try:
                    DogItems.objects.get(reservation = reservation,dog = serializer.validated_data['dog']).delete()
                except Exception as e:
                    return Response({'Object Error' : 'The object didnt exist'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'Object deleted': 'object deleted'}, status=status.HTTP_201_CREATED)
            return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptReservation(APIView):
    permission_classes = (IsAuthenticated, IsWalker)

    def put(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.walker != self.request.user.customer.walker:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'pending':
            serializer = ReservationStatusSerializer(reservation, data= request.data)
            if serializer.is_valid():
                slots = reservation.walker.slots(serializer.validated_data['date'], serializer.validated_data['duration'])
                if slots > 0 and reservation.date > timezone.now():
                    reservation.status = 'accepted'
                    reservation.save()
                    return Response({'Reservation accepted':'accepted'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'Reservation error': 'You cant accept more dogs at that time'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)

class RefuseReservation(APIView):
    permission_classes = (IsAuthenticated, IsWalker)

    def put(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.walker != self.request.user.customer.walker:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'pending':
            serializer = ReservationStatusSerializer(reservation, data= request.data)
            if serializer.is_valid():
                reservation.status = 'refused'
                reservation.save()
                return Response({'Reservation refused':'refused'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)


class CancelReservation(APIView):
    permission_classes = (IsAuthenticated)

    def put(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.walker != self.request.user.customer.walker:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            try:
                if reservation.owner != self.request.user.customer.owner:
                    Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'pending' or reservation.status == 'accepted':
            serializer = ReservationStatusSerializer(reservation, data= request.data)
            if serializer.is_valid():
                reservation.status = 'canceled'
                reservation.save()
                return Response({'Reservation canceled':'canceled'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)


class ConcludeReservation(APIView):
    permission_classes = (IsAuthenticated, IsWalker)

    def put(self,request, pk, format = None):
        reservation = Reservation.objects.get(id = pk)
        try:
            if reservation.walker != self.request.user.customer.walker:
                Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        if reservation.status == 'pending':
            serializer = ReservationStatusSerializer(reservation, data= request.data)
            if serializer.is_valid():
                if reservation.date > timezone.now():
                    reservation.status = 'concluded'
                    reservation.save()
                    return Response({'Reservation concluded':'concluded'}, status=status.HTTP_201_CREATED)
                return Response({'Edit Error' : 'you cant cancel this reservation now'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Edit Error' : 'you cant edit this reservation'}, status=status.HTTP_400_BAD_REQUEST)



class ReservationCreateItem(APIView):
    permission_classes = (IsAuthenticated,IsOwner)
    def post(self, request, format=None):
        serializer = ReservationItemCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
