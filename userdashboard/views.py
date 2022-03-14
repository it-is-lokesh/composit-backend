from django.shortcuts import render
from httplib2 import Response
import userdashboard
from userdashboard.models import userDashboard

# Create your views here.


def registerForEvent(request):
    if request.method == 'POST':
        username = request.data['username']
        eventID = request.data['eventID']

        myuser = userdashboard.objects.all().filter(username=username)
        myuser.events_registered = myuser.events_registered + eventID + ' '
        context = {'success': 1}
        return Response(context)