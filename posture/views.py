import os
import uuid
import json

from django.http import HttpResponse, Http404
from django.shortcuts import render

from posture.static.posture.opencv import base64decode
from posture.static.posture.opencv import opencv
from .models import User

def frontPage(request):
    return render(request, 'posture/frontPage.html')

def captureBaseline(request):
    return render(request, 'posture/captureBaseline.html')

def tracker(request):
    try:
        user_photo_url = request.POST['user_photo_url']
    except:
        raise Http404

    request.session['user_id'] = str(uuid.uuid1())
    user_id = request.session.get('user_id')

    user_baseline_photo = base64decode.base64ToImg(user_photo_url)

    try:
        user_baseline_eyes_height = opencv.get_eyes_height(user_baseline_photo)
    except:
        raise Http404

    User.objects.create(user_id = user_id, user_baseline_photo = user_baseline_photo,
                        user_baseline_eyes_height = user_baseline_eyes_height)

    return render(request, 'posture/tracker.html')

def assertPosture(request):
    try:
        user_photo_url = request.POST['user_photo_url']
    except:
        raise Http404

    user_latest_photo = base64decode.base64ToImg(user_photo_url)
    user_latest_eyes_height = opencv.get_eyes_height(user_latest_photo)

    user_id = request.session.get('user_id')
    user_baseline_eyes_height = User.objects.get(user_id=user_id).user_baseline_eyes_height

    print("baseline: %d" % user_baseline_eyes_height)
    print("latest: %d" % user_latest_eyes_height)

    if (user_latest_eyes_height > user_baseline_eyes_height):
        return HttpResponse("posture_fail")
    else:
        return HttpResponse("posture_pass")

def alertUser(request):
    return render(request, 'posture/alertUser.html')

def webcamWorker(request):
    return render(request, 'posture/webcamWorker.js')