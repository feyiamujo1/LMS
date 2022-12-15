from django.urls import path
from .views import CourseView, CourseDetailView

urlpatterns = [
    path('', CourseView.as_view(), name="course-list"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course-detail")
]