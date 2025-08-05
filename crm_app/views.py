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
        lead = serializer.save(created_by=self.request.user)
        
        # Create log entry for lead creation
        LeadLog.objects.create(
            lead=lead,
            action=LeadLog.ActionChoices.CREATED,
            new_value=lead.status,
            changed_by=self.request.user,
            description=f"Lead created with status '{lead.status}'"
        )
        
        # If lead is created with Converted status, create enrollment
        if lead.status == Lead.StatusChoices.CONVERTED:
            if not Enrollment.objects.filter(lead=lead).exists():
                Enrollment.objects.create(
                    lead=lead,
                    course=lead.course
                )
                LeadLog.objects.create(
                    lead=lead,
                    action=LeadLog.ActionChoices.ENROLLMENT_CREATED,
                    changed_by=self.request.user,
                    description="Enrollment created automatically"
                )
    

class LeadRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        prev_status = instance.status
        prev_next_call = instance.next_call
        prev_last_call = instance.last_call
        prev_remarks = instance.remarks
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        # Log status changes
        if prev_status != updated_lead.status:
            LeadLog.objects.create(
                lead=updated_lead,
                action=LeadLog.ActionChoices.STATUS_CHANGED,
                field_changed='status',
                old_value=prev_status,
                new_value=updated_lead.status,
                changed_by=request.user,
                description=f"Status changed from '{prev_status}' to '{updated_lead.status}'"
            )
            
            # Log if moved to trash
            if updated_lead.status in [Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK]:
                LeadLog.objects.create(
                    lead=updated_lead,
                    action=LeadLog.ActionChoices.MOVED_TO_TRASH,
                    field_changed='status',
                    old_value=prev_status,
                    new_value=updated_lead.status,
                    changed_by=request.user,
                    description=f"Lead moved to trash with status '{updated_lead.status}'"
                )

        # Log next call changes
        if prev_next_call != updated_lead.next_call and 'next_call' in request.data:
            LeadLog.objects.create(
                lead=updated_lead,
                action=LeadLog.ActionChoices.NEXT_CALL_UPDATED,
                field_changed='next_call',
                old_value=str(prev_next_call) if prev_next_call else '',
                new_value=str(updated_lead.next_call) if updated_lead.next_call else '',
                changed_by=request.user,
                description=f"Next Call date changed from '{prev_next_call}' to '{updated_lead.next_call}'"
            )

        # Log last call changes
        if prev_last_call != updated_lead.last_call and 'last_call' in request.data:
            LeadLog.objects.create(
                lead=updated_lead,
                action=LeadLog.ActionChoices.LAST_CALL_UPDATED,
                field_changed='last_call',
                old_value=str(prev_last_call) if prev_last_call else '',
                new_value=str(updated_lead.last_call) if updated_lead.last_call else '',
                changed_by=request.user,
                description=f"Last Call date changed from '{prev_last_call}' to '{updated_lead.last_call}'"
            )

        # Log remarks changes
        if prev_remarks != updated_lead.remarks and 'remarks' in request.data:
            LeadLog.objects.create(
                lead=updated_lead,
                action=LeadLog.ActionChoices.REMARKS_UPDATED,
                field_changed='remarks',
                old_value=prev_remarks[:100] + "..." if len(prev_remarks) > 100 else prev_remarks,
                new_value=updated_lead.remarks[:100] + "..." if len(updated_lead.remarks) > 100 else updated_lead.remarks,
                changed_by=request.user,
                description="Remarks updated"
            )

        # Handle conversion
        if prev_status != Lead.StatusChoices.CONVERTED and updated_lead.status == Lead.StatusChoices.CONVERTED:
            if not Enrollment.objects.filter(lead=updated_lead).exists():
                Enrollment.objects.create(
                    lead=updated_lead,
                    course=updated_lead.course
                )
                LeadLog.objects.create(
                    lead=updated_lead,
                    action=LeadLog.ActionChoices.ENROLLMENT_CREATED,
                    changed_by=request.user,
                    description="Enrollment created upon conversion"
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
    serializer_class = TrashLeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show leads with lost or junk status
        return Lead.objects.filter(status__in=[Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK])
    

class TrashRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrashLeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow operations on leads in trash (lost or junk)
        return Lead.objects.filter(status__in=[Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        prev_status = instance.status
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_lead = serializer.save()

        # Log restoration from trash
        if prev_status in [Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK] and updated_lead.status not in [Lead.StatusChoices.LOST, Lead.StatusChoices.JUNK]:
            LeadLog.objects.create(
                lead=updated_lead,
                action=LeadLog.ActionChoices.RESTORED,
                field_changed='status',
                old_value=prev_status,
                new_value=updated_lead.status,
                changed_by=request.user,
                description=f"Lead restored from trash. Status changed from '{prev_status}' to '{updated_lead.status}'"
            )
        
        return Response(serializer.data)


# Add a view to get logs for a specific lead
class LeadLogListView(generics.ListAPIView):
    serializer_class = LeadLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        lead_id = self.kwargs.get('lead_id')
        return LeadLog.objects.filter(lead_id=lead_id)


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