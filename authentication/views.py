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
    return render(request, 'authentication/index.html')


# staticNova
# lokesh


@api_view(['GET', 'POST', 'OPTIONS'])
def signup(request):
    if request.method == 'GET':
        db = userDashboard.objects.all()
        serializer = userDashboardSerializer(db, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data['username']
        name = request.data['name']
        email = request.data['email']
        number = request.data['number']
        collegeName = request.data['collegeName']
        password = request.data['password']

        userNameCheck = User.objects.filter(username=username)
        emailCheck = User.objects.filter(email=email)

        if not len(userNameCheck) and not len(emailCheck):
            ins = userDashboard(username=username, name=name, email=email,
                                number=number, collegeName=collegeName)
            ins.save()

            if(1):
                decoderObj = decoder()
                connection = EmailBackend(
                    host='smtp.gmail.com',
                    port=587,
                    username='noreplycomposit2022@gmail.com',
                    password='composit@2022'
                )

                myuser = User.objects.create_user(
                    username=username, email=email, password=password)
                myuser.first_name = name
                myuser.last_name = ''
                myuser.is_active = False
                myuser.save()
                body = render_to_string('email_verification.html', {
                    'user': myuser,
                    'domain': 'composit-api.herokuapp.com',
                    'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                    'token': account_activation_token.make_token(myuser),
                })
                emailSender = EmailMessage(
                    'Composit Registration confirmed',
                    body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    bcc='sailokesh.gorantla@ecell-iitkgp.org'
                    connection=connection
                )
                emailSender.fail_silently = False
                emailSender.send()
            if(1):
                context = {
                    'success': 1,
                    'userNameExists': 0,
                    'emailExists': 0,
                }
                context = json.dumps(context)
                return Response(context)
        if len(userNameCheck):
            context = {
                'success': 0,
                'emailExists': 0,
                'userNameExists': 1,
            }
            context = json.dumps(context)
            print(context)
            return Response(context)
        if len(emailCheck):
            context = {
                'success': 0,
                'emailExists': 1,
                'userNameExists': 0,
            }
            context = json.dumps(context)
            print(2, context)
            return Response(context)
    return Response({'fail': 1})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'verification.html')
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
            #  £¤pb`bb 10 3 2022
            getUserDetails = userDashboard.objects.filter(username=username)
            context = {
                'userRegistered': 'true',
                'name': str(getUserDetails[0].name),
                'collegeName': str(getUserDetails[0].collegeName),
                'username': str(getUserDetails[0].username),
                'number': str(getUserDetails[0].number),
                'email': str(getUserDetails[0].email),
                'eventsRegistered': str(getUserDetails[0].events_registered),
                'date': str(getUserDetails[0].datestamp),
            }
            print(context)
            return Response(context)
        elif user is None:
            context = {
                'userRegistered': 'false',
            }
            return Response(context)


def signout(request):
    logout(request)
    messages.success(request, 'U are logged out!')
    return redirect('home')
