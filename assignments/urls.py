from django.urls import path
from .views import AssignmentDetailView, AssignmentView

urlpatterns = [
    path("", AssignmentView.as_view(), name='assignment-list'),
    path("<int:pk>/", AssignmentDetailView.as_view(), name='assignment-detail')
]