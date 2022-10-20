from django.urls import path
from .views import StudentDetailView, StudentListCreateView, ClassStudentCreateListView, ClassStudentDetailView

urlpatterns = [
    path('', StudentListCreateView.as_view(), name='student-create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('studentships/', ClassStudentCreateListView.as_view(), name='studentships'),
    path('studentships/<int:pk>/', ClassStudentDetailView.as_view(), name='studentship-detail')
]