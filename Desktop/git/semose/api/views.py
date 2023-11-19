from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Place
from rest_framework.decorators import api_view
from .serializers import PlaceSerializer
import pandas as pd
from .dis_min import haversine, change_min
from .change import get_lat_lng_from_address
from .Query_condition import QuerySemose, distance_weight, score_accesibility
import json

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

# Cache
from django.core.cache import cache

# Logging
from .models import LogEntry
from .serializers import LogEntrySerializer
from rest_framework import status

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@api_view(['GET'])
def index2(request):
    if request.method == 'GET':
        place = Place.objects.all()
        serializer = PlaceSerializer(place, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})

class DataView(APIView):
    def get(self, request,
            address=cache.get('address_data'),
            shop_lst=cache.get('selected_data'), 
            minutes=30, 
            first=True):
        
        shop_lst = json.loads(shop_lst)
        print(address, shop_lst)
        score = score_accesibility(address, shop_lst)
        scorebox = {'score':score}
        return Response(scorebox)
    
    def post(self, request):
        # POST 데이터를 JSON 형식으로 받아옵니다.
        data = request.data

        # 필요한 데이터 추출
        address = data.get("address")
        selected = data.get("selected", [])

        # 이제 `address`와 `selected`를 캐시
        cache.set('address_data', address)
        cache.set('selected_data', selected)
        
        # 결과 데이터를 응답으로 반환
        response_data = {"message": "Data received successfully."}
        return Response(response_data)
    

class LogEntryView(APIView):
    def post(self, request):
        data = request.data
        serializer = LogEntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
