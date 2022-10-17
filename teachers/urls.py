from django.urls import path
from .views import TeacherCreateView

urlpatterns = [
    path('teachers/', TeacherCreateView.as_view()),
]