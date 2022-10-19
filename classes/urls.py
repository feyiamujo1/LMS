from django.urls import path
from .views import ClassView, ClassDetailView

urlpatterns = [
    path('', ClassView.as_view(), name="class-list"),
    path("<int:pk>/", ClassDetailView.as_view(), name="class-detail")
]