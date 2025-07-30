from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        current_user = request.user
        requested_role = request.data.get('role')

        # Superadmin can create admin and sales_rep
        if current_user.role == User.Roles.SUPERADMIN:
            if requested_role not in [User.Roles.ADMIN, User.Roles.SALES_REP]:
                return Response({'error': 'Superadmin can only create admin or sales_rep.'}, status=status.HTTP_403_FORBIDDEN)
        # Admin can only create sales_rep
        elif current_user.role == User.Roles.ADMIN:
            if requested_role != User.Roles.SALES_REP:
                return Response({'error': 'Admin can only create sales_rep.'}, status=status.HTTP_403_FORBIDDEN)
        # Sales rep cannot create users
        else:
            return Response({'error': 'Sales rep cannot create users.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': f'{requested_role.replace("_", " ").title()} registered successfully.'}, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        current_user = self.request.user

        # Superadmin can edit/delete admin and sales_rep
        if current_user.role == User.Roles.SUPERADMIN:
            if obj.role not in [User.Roles.ADMIN, User.Roles.SALES_REP]:
                raise permissions.PermissionDenied("Superadmin can only manage admin or sales_rep.")
        # Admin can edit/delete sales_rep only
        elif current_user.role == User.Roles.ADMIN:
            if obj.role != User.Roles.SALES_REP:
                raise permissions.PermissionDenied("Admin can only manage sales_rep.")
        # Sales rep cannot edit/delete any user
        else:
            raise permissions.PermissionDenied("Sales rep cannot manage users.")
        return obj