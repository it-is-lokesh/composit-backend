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
from authentication.decrypter import decoder
from django.core.mail.backends.smtp import EmailBackend


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token


def home(request):
    return render(request, "authentication/index.html")


@api_view(['GET', 'POST', 'OPTIONS'])
def signup(request):
    if request.method == 'GET':
        db = userDashboard.objects.all()
        serializer = userDashboardSerializer(db, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        username = request.data['username']
        name = request.data['name']
        email = request.data['email']
        number = request.data['number']
        # city = request.data['city']
        collegeName = request.data['collegeName']
        password = request.data['password']

        userNameCheck = userDashboard.objects.filter(username=username)
        emailCheck = userDashboard.objects.filter(email=email)

        if not len(userNameCheck) and not len(emailCheck):
            ins = userDashboard(username=username, name=name, email=email,
                                number=number, collegeName=collegeName)
            ins.save()

            decoderObj = decoder()
            connection = EmailBackend(
                host='smtp.gmail.com',
                port=587,
                username='sailokesh.gorantla@ecell-iitkgp.org',
                password=decoderObj.decode('k][]] 3 3 2022')
            )

            myuser = User.objects.create_user(
                username=username, email=email, password=password)
            myuser.first_name = name
            myuser.last_name = ''
            myuser.save()
            print(account_activation_token.make_token(type(myuser)))
            body = ''
            emailSender = EmailMessage(
                'Composit Registration confirmed',
                body,
                settings.EMAIL_HOST_USER,
                [email, 'sailokesh.gorantla@ecell-iitkgp.org'],
                connection=connection
            )
            emailSender.fail_silently = False
            emailSender.send()
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
            print("0", context)
            return Response(context)
        if len(userNameCheck):
            context = {
                'success': 'false',
                'emailExists': 'false',
                'userNameExists': 'true',
            }
            context = json.dumps(context)
            print("1", context)
            return Response(context)
        if len(emailCheck):
            context = {
                'success': 'false',
                'emailExists': 'true',
                'userNameExists': 'false',
            }
            context = json.dumps(context)
            print("2", context)
            return Response(context)
    return Response({'fail': 'true'})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('Thank you for your email confirmation. Now you can login your account.')
    else:
        return Response('Activation link is invalid!')


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

        if user is not None:
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
