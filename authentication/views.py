from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from userdashboard.models import userDashboard
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from userdashboard.serializers import userDashboardSerializer
from authentication.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


def home(request):
    return render(request, "authentication/index.html")


@api_view(['GET', 'POST', 'OPTIONS'])
def signup(request):
    if request.method == 'GET':
        db = userDashboard.objects.all()
        serializer = userDashboardSerializer(db, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        c = {'s': False}
        username = request.data['username']
        name = request.data['name']
        email = request.data['email']
        number = request.data['number']
        collegeName = request.data['collegeName']
        password = request.data['password']

        userNameCheck = userDashboard.objects.filter(username=username)
        emailCheck = userDashboard.objects.filter(email=email)

        if not len(userNameCheck) and not len(emailCheck):
            ins = userDashboard(username=username, name=name,
                                email=email, number=number, collegeName=collegeName)
            ins.save()

            myuser = User.objects.create_user(
                username=username, email=email, password=password)
            myuser.first_name = name
            myuser.last_name = ''
            myuser.save()
            body = render_to_string(
                'authentication/email.html', {'name': name})
            email = EmailMessage(
                'ECell Round 3 Selections | Meeting Link',
                body,
                settings.EMAIL_HOST_USER,
                [email, 'sailokesh.gorantla@ecell-iitkgp.org'],
            )
            email.fail_silently = False
            email.send()
            context = {
                'success': 'True',
                'userNameExists': 'False',
                'emailExists': 'False',
                'username': username,
                'name': name,
                'collegaName': collegeName,
                'number': number,
                'email': email,
                'eventsRegistered': '',
            }
            return Response(context)
        if len(userNameCheck):
            context = {
                'success': 'False',
                'userNameExists': 'True',
            }
            return Response(context)
        if len(emailCheck):
            context = {
                'success': 'False',
                'emailExists': 'True'
            }
            return Response(context)
    return Response({'fail': 'True'})


@api_view(['GET', 'POST', 'OPTIONS'])
def signin(request):
    if request.method == 'GET':
        db = userDashboard.objects.all()
        serializer = userDashboardSerializer(db, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if not len(user):
            getUserDetails = userDashboard.objects.filter(username=username)
            context = {
                'userRegistered': True,
                'name': getUserDetails[0].name,
                'collegeName': getUserDetails[0].collegeName,
                'username': getUserDetails[0].username,
                'number': getUserDetails[0].number,
                'email': getUserDetails[0].email,
                'eventsRegistered': getUserDetails[0].events_registered,
            }
            return Response(context)
        else:
            context = {
                'userRegistered': False,
            }
            return Response(context)

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "U are logged out!")
    return redirect('home')
