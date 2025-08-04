from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),  # login, logout, password reset

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail-update-destroy'),

    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail-update-destroy'),

    path('leads/', LeadListCreateView.as_view(), name = 'lead-list-create'),
    path('leads/<int:pk>/', LeadRetrieveUpdateDestroyView.as_view(), name='lead-retrieve-update-destroy'),

    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', EnrollmentRetrieveUpdateDestroyView.as_view(), name='enrollments-update-retrieve-destroy'),

    path('trash/', TrashListView.as_view(), name='trash-list'),
    path('trash/<int:pk>/', TrashRetrieveUpdateDestroyView.as_view(), name='trash-detail')
    # for restore / delete
]