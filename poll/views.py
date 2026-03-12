from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, Vote
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer


# API - QUESTION LIST
@api_view(['GET'])
def question_list_api(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


# API - VOTE
@api_view(['POST'])
def vote_api(request):

    choice_id = request.data.get('choice_id')
    user_id = request.data.get('user_id')

    try:
        choice = Choice.objects.get(id=choice_id)
        user = User.objects.get(id=user_id)

        # prevent duplicate vote
        if Vote.objects.filter(user=user, question=choice.question).exists():
            return Response({"error": "Already voted"})

        Vote.objects.create(
            user=user,
            question=choice.question,
            choice=choice
        )

        choice.votes += 1
        choice.save()

        return Response({"message": "Vote submitted successfully"})

    except Choice.DoesNotExist:
        return Response({"error": "Choice not found"})

@api_view(['POST'])
def login_api(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error':'User not found'})

    user = authenticate(username=user.username,password=password)

    if user is not None:
        return Response({
            "user_id": user.id,
            "email": user.email
        })

    return Response({"error":"Invalid password"})
@api_view(['POST'])
def register_api(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        return Response({'error':'Email already exists'})

    username = email.split('@')[0]

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message": "Register success",
        "user_id": user.id,
        "email": user.email
    })
# LOGIN
def custom_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and Password required")
            return redirect("login")

        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            messages.error(request, "Email does not exist")
            return redirect("login")

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Incorrect password")
            return redirect("login")

    return render(request, "poll/login.html")


# INDEX PAGE
def index(request):
    questions = Question.objects.all()
    return render(request, 'poll/index.html', {'questions': questions})


# REGISTER
def register(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        if not email or not password:
            messages.error(request, "Email and Password required")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        if not username:
            username = email

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'poll/register.html')

@login_required
def vote(request, question_id):

    if request.method != "POST":
        return redirect('index')

    question = get_object_or_404(Question, pk=question_id)
    questions = Question.objects.all()
    choice_id = request.POST.get('choice')

    if not choice_id:
        questions = Question.objects.all()
        return render(request, "poll/index.html", {
            "questions": questions,
            "error_message": "Please select a choice",
            "message_type": "error",
            "error_question_id": question.id
        })

    # already voted check
    if Vote.objects.filter(user=request.user, question=question).exists():
        questions = Question.objects.all()
        return render(request, "poll/index.html", {
            "questions": questions,
            "error_message": "You have already voted for this question",
            "message_type": "error",
            "error_question_id": question.id
        })

    selected_choice = get_object_or_404(Choice, pk=choice_id)

    Vote.objects.create(
        user=request.user,
        question=question,
        choice=selected_choice
    )

    selected_choice.votes += 1
    selected_choice.save()

    # success message under same question
    return render(request, "poll/index.html", {
        "questions": questions,
        "error_message": "Vote submitted successfully",
        "message_type": "success",
        "error_question_id": question.id,
        "success" : "200"
    })