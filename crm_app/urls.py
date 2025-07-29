from django.urls import path
from .views import AdminListCreateView, SalesRepListCreateView

urlpatterns = [
    path('admin/', AdminListCreateView.as_view(), name='admin-list-create'),
    path('sales-rep/', SalesRepListCreateView.as_view(), name='salesrep-list-create'),
]