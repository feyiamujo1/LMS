from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, 
    CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView)
from rest_framework.views import APIView
from .models import Quiz, Question, AnswerChoice, Answer, QuizSolution, Score
from .serializers import (QuizCreateSerializer, QuestionCreateSerializer,
     AnswerCreateSerializer, QuizSolutionCreateSerializer, AnswerChoiceSerializer,
      ScoreSerializer, QuestionListSerializer,
      QuizUpdateSerializer, QuizWithQuestionsSerializer, RemoveQuestionSerializer,
      QuizClassGetSerializer)
from teachers.models import TeacherProfile
from users import authentication
from rest_framework import authentication as r_auth
from .permissions import IsAdminOrTeacherPermission
from rest_framework import serializers, status
from rest_framework.response import Response
# Create your views here.

class QuizAPIView(ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizCreateSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        r_auth.BasicAuthentication,
        r_auth.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        if self.request.user.role == "STAFF":
            serializer.save(created_by=TeacherProfile.objects.get(user=self.request.user))
        else:
            return

class QuizUpdateView(RetrieveUpdateAPIView):
    """
    Updates Quiz name with questions

    Request:
    data = {
    'name': "General Knowledge
    'question_ids': [3,4]
    }

    Responses:
    {
        'name': 'General Knowledge', 
        'questions': [3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 24, 26, 27, 31, 32, 33, 34, 35], 
        'created_by': 'Teacher taslim@django.core', 
        'created_for': 
        'Physics, 2019/2020', 
        'date_created': '2022-12-12T13:33:03.659028Z', 
        'last_updated': '2022-12-14T09:53:36.238158Z'
    }

    {
        'detail': 'Not found'
    }
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizUpdateSerializer

    def update(self, request, *args, **kwargs):
        data = self.request.data
        obj = Quiz.objects.filter(id=kwargs['pk']).first()
        if hasattr(obj, 'id'):
            if 'question_ids' in data:
                for num in data['question_ids']:
                    q = Question.objects.filter(id=num).first()
                    if hasattr(q, 'id'):
                        obj.questions.add(q)
                    else:
                        raise serializers.ValidationError("Question not found")
        else:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer

class QuestionCreateAPIView(ListCreateAPIView):
    """
    Request:
    {
        'body': "Don't throw stones at _____ houses.",
        'answer': 'glass',
        'incorrect_answers' : ['mud', 'tree', 'concrete'],
        'quiz_id' : 1
    }

    Response:
    {
        'body': "Don't throw stones at _____ houses.", 
        'correct_answer': 'glass', 'incorrect_answers': [
        {'91': 'mud'}, {'92': 'tree'}, {'93': 'concrete'}]
    }
    """
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAdminOrTeacherPermission]
    authentication_classes = [
        authentication.TokenAuthentication,
        r_auth.BasicAuthentication,
        r_auth.SessionAuthentication,
    ]
    
    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        serializer = QuestionListSerializer(questions, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            # print(serializer.validated_data)
            data = self.request.data
            current_teacher = TeacherProfile.objects.get(user=self.request.user)
            correct_answer = AnswerChoice.objects.create(created_by=current_teacher, body=serializer.validated_data.get('answer'))
            correct_answer.save()
            correct_answer.refresh_from_db()
            question = Question.objects.create(created_by=current_teacher, body=serializer.validated_data.get('body'), correct_answer=correct_answer)
            question.correct_answer = correct_answer
            # print(serializer.validated_data.get('incorrect_answers'))
            if 'incorrect_answers' in serializer.validated_data:
                for ans in serializer.validated_data.get('incorrect_answers'):
                    incorrect_answer = AnswerChoice.objects.create(created_by=current_teacher, body=ans)
                    incorrect_answer.save()
                    incorrect_answer.refresh_from_db()
                    question.incorrect_answers.add(incorrect_answer)
            question.save()
            if 'quiz_id' in data:
                quiz = Quiz.objects.filter(id=data['quiz_id']).first()
                quiz.questions.add(question)
            serializer_data = QuestionListSerializer(question).data
            return serializer_data
        else:
            return Response(serializer.errors,status=400)

class QuizCreateWithMultipleQuestions(APIView):
    """
    Request:
    {
        "quiz_id": 1,
        "questions": [
            {'body': 'How many planets are there?',
            'answer': 'more than 9',
            'incorrect_answers':[
                'three','nine','eight'
                ]},
            {'body': 'which of the following is not considered queer?',
            'answer': 'heterosexual',
            'incorrect_answers':[
                'transgender','gay','bisexual'
                ]}
            ]
    }

    Response:

    {
        'quiz_id': 1, 
        'questions': [
            {'body': 'How many planets are there?', 
                'correct_answer': 'more than 9', 
                'incorrect_answers': [
                    {'95': 'three'}, {'96': 'nine'}, {'97': 'eight'}
                    ]},
            {'body': 'which of the following is not considered queer?', 
                'correct_answer': 'heterosexual', 
                'incorrect_answers': [
                    {'99': 'transgender'}, {'100': 'gay'}, {'101': 'bisexual'}
                    ]}
                ]
    }
    """
    serializer_class = QuizWithQuestionsSerializer
    def get(self, request):
        quizzes = Quiz.objects.all()
        return Response(QuizCreateSerializer(quizzes, many=True, context={'request':request}).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        questions = self.request.data['questions']
        quiz_id = self.request.data['quiz_id']
        teacher = TeacherProfile.objects.get(user=self.request.user)
        response = {
                    'quiz_id':quiz_id,
                    'questions' : [],
                    }
        for question in questions:
            saved_question=QuestionCreateAPIView.perform_create(self, serializer=QuestionCreateSerializer(data=question))
            response['questions'].append(saved_question)
        return Response(response, status=status.HTTP_201_CREATED)
    

class RemoveQuestionFromQuizView(APIView):
    # serializer_class = RemoveQuestionSerializer
    """
    Request:
    {
        "questions":
        [2,3,7,8,9,10,11,12,13,14,15,16,17]
    }

    """
    def get(self, request, **kwargs):
        quiz = Quiz.objects.filter(id=kwargs['pk']).first()
        if hasattr(quiz, 'id'):
            return Response(QuizCreateSerializer(quiz, context={'request': request}, many=False).data, status=status.HTTP_200_OK)
        return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, **kwargs):
        quiz = Quiz.objects.filter(id=kwargs['pk']).first()
        if hasattr(quiz, 'id'):
            if 'questions' in request.data:
                for id in request.data['questions']:
                    question =  Question.objects.get(id=id)
                    if hasattr(question, 'id') and question in quiz.questions.all():
                        quiz.questions.remove(question)
                        quiz.refresh_from_db()
                    else:
                        # return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
                        continue
            return Response(QuizCreateSerializer(quiz, context={'request': request}, many=False).data, status=status.HTTP_202_ACCEPTED)
        return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)

class GetQuizzesByCreatorWithClass(APIView):
    serializer_class = QuizClassGetSerializer
    def get(self, request, *args, **kwargs):
        data = Quiz.objects.filter(created_by=TeacherProfile.objects.get(user=request.user.id), created_for=request.data['class_id']).all()
        return Response(QuizCreateSerializer(data, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class AnswerCreateAPIView(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

class QuizSolutionAPIView(ListCreateAPIView):
    queryset = QuizSolution.objects.all()
    serializer_class = QuizSolutionCreateSerializer

class AnswerChoiceAPIView(ListCreateAPIView):
    queryset = AnswerChoice.objects.all()
    serializer_class = AnswerChoiceSerializer

class ScoreAPIView(ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer