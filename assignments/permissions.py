from rest_framework import permissions
from teachers.models import TeacherProfile

class IsStaffAssignmentOwnerOrCoStaff(permissions.DjangoModelPermissions, permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        if obj.given_by == teacher_id or obj.given_to == teacher_id.courses:
            return True
    
    def has_permission(self, request, view):
        return request.user.role == "STAFF" or request.user.role == "ADMIN"
        
        
