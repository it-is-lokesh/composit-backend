from httplib2 import Response
import userdashboard
from django.http import HttpResponse
import json

# Create your views here.


def registerForEvent(request):
    if request.method == 'GET':
        return HttpResponse("Not authorised")

    if request.method == 'POST':
        username = request.data['username']
        eventID = request.data['eventID']

        myuser = userdashboard.objects.all().filter(username=username)
        myuser.events_registered = myuser.events_registered + eventID + ' '
        print(myuser.events_registered)
        context = {'success': 1}
        context = json.dumps(context)
        return Response(context)