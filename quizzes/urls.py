from django.urls import path
from .views import (QuizAPIView, QuestionCreateAPIView, AnswerCreateAPIView, 
        QuizSolutionAPIView, AnswerChoiceAPIView, QuestionListAPIView,
        QuizUpdateView, QuizCreateWithMultipleQuestions)

urlpatterns = [
    path('create/', QuizAPIView.as_view(), name="quiz-create"),
    path('update/<int:pk>', QuizUpdateView.as_view(), name="quiz-update"),
    path('create_with_questions/', QuizCreateWithMultipleQuestions.as_view(), name="quiz-create-questions"),
    path('questions/create/', QuestionCreateAPIView.as_view(), name="question-create"),
    path('questions/list/', QuestionListAPIView.as_view(), name='question-list'),
    path('answer/create/', AnswerCreateAPIView.as_view(), name="answer-create"),
    path('solution/create/', QuizSolutionAPIView.as_view(), name="solution-create"),
    path('answer_choice/create', AnswerChoiceAPIView.as_view(), name="answer-choice-create")
]
