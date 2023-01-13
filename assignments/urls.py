from django.urls import path
from .views import AssignmentDetailView, AssignmentView, GetAssignmentsGivenToClassByTeacher, SolutionListCreateView

urlpatterns = [
    path("", AssignmentView.as_view(), name='assignment-list'),
    path("teacher/class", GetAssignmentsGivenToClassByTeacher.as_view(), name="assignment-teacher-class"),
    path("<int:pk>/", AssignmentDetailView.as_view(), name='assignment-detail'),
    path("solutions/", SolutionListCreateView.as_view(), name="solution-view")
]