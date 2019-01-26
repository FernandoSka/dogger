from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ReservationSerializer,
    CheckSlotSerializer,
    ReservationItemSerializer,
    ReservationItemCreateSerializer,
)
from rest_framework.permissions import IsAuthenticated

class ReservationDetail(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ReservationSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationCreateItem(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ReservationItemCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
