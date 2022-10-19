from django.urls import path
from .views import StudentDetailView, StudentListCreateView

urlpatterns = [
    path('', StudentListCreateView.as_view(), name='student-create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail')
]