from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username':user.username,
            'FirstName':user.first_name,
            'LastName':user.last_name
        })


# list of vendors/ create a new vendor
class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            if not queryset.exists():
                return Response({"message": "No vendors found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({'data':serializer.data, 'success':True},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)})
            
class VendorCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exceptions=True)
            serializer.save()
            return Response({'data':serializer.data, 'success':True},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)})

    
class VendorListCreateView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response({"message": "No vendors found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'data':serializer.data, 'success':True},status=status.HTTP_200_OK)
    
# retrieve details/update a specific vendor/ delete a specific vendor
class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


# list of purchase orders/create a new purchase order
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response({"message": "No purchase order found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


# retrieve details/ update a specific purchase order/ delete a specific purchase order
class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


# retrieve performance details of specific vendor
class VendorPerformanceRetrieveView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_url_kwarg = 'vendor_id'
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


# Acknowledge the receipt of a purchase order
class AcknowledgeUpdate(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.validated_data['acknowledgment_date'] = timezone.now()
        super().perform_update(serializer)
        return Response(serializer.data)
