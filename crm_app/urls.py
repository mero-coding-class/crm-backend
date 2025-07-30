from django.urls import path
from .views import *

urlpatterns = [
    # register admin and sales representative
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail-update-destroy'),

    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail-update-destroy'),

    path('leads/', LeadListCreateView.as_view(), name = 'lead-list-create'),
    path('leads/<int:pk>/', LeadRetrieveUpdateDestroyView.as_view(), name='lead-retrieve-update-destroy'),
]