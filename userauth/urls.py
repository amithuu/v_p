from django.urls import path
from .views import *
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    # path('token/', UserTokenAPIView.as_view(), name='user_token'),
    
    # Vendor URLs
    path('api/vendors/create/', VendorCreateView.as_view(), name='vendor-create'),
    path('api/vendors/list/', VendorListView.as_view(), name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),

    # Purchase Order URLs
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase-order-retrieve-update-destroy'),

    # Vendor Performance URLs
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceRetrieveView.as_view(), name='vendor-performance-retrieve'),
    path('api/purchase_orders/<int:pk>/acknowledge/', views.AcknowledgeUpdate.as_view()),

    path('login/', CustomAuthToken.as_view())
]