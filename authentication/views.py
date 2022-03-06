from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from userdashboard.models import userDashboard
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from userdashboard.serializers import userDashboardSerializer
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.conf import settings
import json

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
                'success': 'true',
                'userNameExists': 'false',
                'emailExists': 'false',
                'username': str(username),
                'name': str(name),
                'collegaName': str(collegeName),
                'number': str(number),
                'email': str(email),
                'eventsRegistered': '',
            }
            context = json.dumps(context)
            return Response(context)
        if len(userNameCheck):
            context = {
                'success': 'false',
                'userNameExists': 'true',
            }
            return Response(context)
        if len(emailCheck):
            context = {
                'success': 'false',
                'emailExists': 'true'
            }
            return Response(context)
    return Response({'fail': 'true'})


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
                'userRegistered': 'true',
                'name': str(getUserDetails[0].name),
                'collegeName': str(getUserDetails[0].collegeName),
                'username': str(getUserDetails[0].username),
                'number': str(getUserDetails[0].number),
                'email': str(getUserDetails[0].email),
                'eventsRegistered': str(getUserDetails[0].events_registered),
            }
            print(context)
            return Response(context)
        elif user is None:
            context = {
                'userRegistered': 'false',
            }
            return Response(context)
        else:
            return Response({'test': 'testw'})


def signout(request):
    logout(request)
    messages.success(request, "U are logged out!")
    return redirect('home')
