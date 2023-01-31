from django.urls import path
from .views import CourseView, CourseDetailView, CoursesWithAssignment, CoursesWithQuizzes

urlpatterns = [
    path('', CourseView.as_view(), name="course-list"),
    path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
    path("courses_with_assignments/", CoursesWithAssignment.as_view(), name="courses-with-assignment"),
    path("courses_with_quizzes/", CoursesWithQuizzes.as_view(), name="courses-with-quiz")
]