from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer

class AdminListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role=User.Roles.ADMIN)
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.role != User.Roles.SUPERADMIN:
            return Response({'error': 'Only superadmin can create admin.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['role'] = User.Roles.ADMIN
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Admin registered successfully.'}, status=status.HTTP_201_CREATED)

class SalesRepListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role=User.Roles.SALES_REP)
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.role not in [User.Roles.SUPERADMIN, User.Roles.ADMIN]:
            return Response({'error': 'Only superadmin or admin can create sales rep.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['role'] = User.Roles.SALES_REP
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Sales rep registered successfully.'}, status=status.HTTP_201_CREATED)