from distutils.command.config import config
from unittest import result
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from interpolation_1.interpolate import interpolate_convert, interpolate_function, OutlierDetector, balance_imbalance
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from interpolation_1.serializers import UserSerializer, GroupSerializer
import json


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def interpolate(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method', status=403)
    if request.method == 'POST':
        all_data = JSONParser().parse(request)
        data_series = all_data['data']
        config = all_data['config']
        result = interpolate_function(data_series, config)

    return HttpResponse( json.dumps( result ) )

@csrf_exempt
def convert_date_interpolate(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method', status=403)
    if request.method == 'POST':
        all_data = JSONParser().parse(request)
        data_series = all_data['data']
        config = all_data['config']
        result = interpolate_convert(data_series, config)

    return HttpResponse( json.dumps( result ) )

@csrf_exempt
def outlier(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method', status=403)
    if request.method == 'POST':
        all_data = JSONParser().parse(request)
        data_series = all_data['data']
        config = all_data['config']

        import pandas as pd 

        series = pd.DataFrame(data_series)
        config = pd.Series(config)

        ts_detector = False
        if config.time_series: 
            ts_detector = True
            series = series.set_index(series.time).drop('time', axis=1)
        else: 
            series = series.set_index(series.id).drop('id', axis=1)

        feature = series.feature.copy()

        result = OutlierDetector(series, config, feature)
    return HttpResponse( result  )

@csrf_exempt
def balance_data(request):
    if request.method == 'GET':
        return HttpResponse('Invalid request method', status=403)
    if request.method == 'POST':
        all_data = JSONParser().parse(request)
        data_series = all_data['data']
        config = all_data['config']

        import pandas as pd 

        series = pd.DataFrame(data_series)
        config = pd.Series(config)

        result = balance_imbalance(series, config)
        
    return HttpResponse( json.dumps(result)  )
