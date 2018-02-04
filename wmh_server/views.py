from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from wmh_server.models import LocationData as lc
from django.views.decorators.csrf import csrf_exempt
import json
import datetime as dt
from django.conf import settings

def index(request):
    res = "Base Path:{}. This is a site of 'WalkMeHome' Project. The site is under construction!".format(settings.BASE_DIR)
    return HttpResponse(res)

@csrf_exempt
def send_loc(request):
    try:
        if (request.method == 'POST') \
                and ('email' in request.POST) \
                and ('loc_date' in request.POST) \
                and ('LAT' in request.POST) \
                and ('LON' in request.POST):
            loc_date_str = request.POST['loc_date']
            loc_date = dt.datetime.strptime(loc_date_str,"%d.%m.%Y %H:%M:%S")
            loc = lc(email=request.POST['email'], loc_date=loc_date, LON=float(request.POST['LON']), LAT=float(request.POST['LAT']))
            loc.save()
            res = "0"
        else:
            res = "Ошибка"
    except NameError:
        res = "Ошибка"

    return HttpResponse(res)

@csrf_exempt
def send_track(request):
    try:
        if (request.method == 'POST'):
            json_data = request.read()
            # json_data contains the data uploaded in request
            data = json.loads(json_data)
            for rec in data:
                loc_date_str = rec['loc_date']
                loc_date = dt.datetime.strptime(loc_date_str,"%d.%m.%Y %H:%M:%S")
                loc = lc(email=rec['email'], loc_date=loc_date, LON=float(rec['LON']), LAT=float(rec['LAT']))
                loc.save()
            res = "0"
        else:
            res = "Ошибка"
    except NameError:
        res = "Ошибка"

    return HttpResponse(res)

@csrf_exempt
def get_last_location(request):
    if (request.method == 'GET') and ('email' in request.GET):
        locations = lc.objects.filter(email=request.GET['email'])
        if locations.count()>0:
            sortlocations = locations.order_by("-loc_date")
            last_record = sortlocations[0]
            loc_date_str = last_record.loc_date.strftime("%d.%m.%Y %H:%M:%S")
            last_location = dict(email=last_record.email, loc_date=loc_date_str,
                                 LAT=last_record.LAT,
                                 LON=last_record.LON)

            res = json.dumps(last_location)
        else:
            res = 'Нет данных'
    else:
        res = 'Ошибка'
    return HttpResponse(res)