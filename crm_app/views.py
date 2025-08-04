from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Course, Enrollment
from .serializers import *
from .permissions import IsSuperadminOrAdmin
from rest_framework.decorators import action

class LeadListCreateView(generics.ListCreateAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show leads that are not converted
        return Lead.objects.exclude(status__in=[Lead.StatusChoices.CONVERTED, Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK])
    
    def perform_create(self, serializer):
        lead = serializer.save()
        # If lead is created with Converted status, create enrollment
        if lead.status == Lead.StatusChoices.CONVERTED:
            if not Enrollment.objects.filter(lead=lead).exists():
                Enrollment.objects.create(
                    lead=lead,
                    course=lead.course
                )


class LeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        prev_status = instance.status
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        if prev_status != Lead.StatusChoices.CONVERTED and updated_lead.status == Lead.StatusChoices.CONVERTED:
            if not Enrollment.objects.filter(lead=updated_lead).exists():
                Enrollment.objects.create(
                    lead=updated_lead,
                    course=updated_lead.course
                )
        return Response(serializer.data)


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSuperadminOrAdmin]

    
class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSuperadminOrAdmin]


class EnrollmentListView(generics.ListAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnrollmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrashListView(generics.ListAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show leads with lost or junk status
        return Lead.objects.filter(status__in=[Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK])
    

class TrashRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow operations on leads in trash (lost or junk)
        return Lead.objects.filter(status__in = [Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK])

    def update(self, request, *args, **kwargs):
        # Handle restoring leads or updating trash items
        return super().update(request, *args, **kwargs)

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