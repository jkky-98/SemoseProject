from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import pandas as pd
from .dis_min import haversine, change_min
from .change import get_lat_lng_from_address
from .Query_condition import QuerySemose, distance_weight, score_accesibility, serve_latlng
from .bus_dis import get_bus_nearby
import json
from .zicbang import oneroom, oneroom_df
import joblib
from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
# Create your views here.

# Cache
from django.core.cache import cache

# Logging
from rest_framework import status

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@api_view(['GET'])
def index2(request):
    return JsonResponse({'message': 'hello world'}, status=status.HTTP_200_OK)

class DataView(APIView):
    def post(self, request):
        # POST 데이터를 JSON 형식으로 받아옵니다.
        data = request.data

        # 필요한 데이터 추출
        address = data.get("address")
        selected = data.get("selected", [])
        lat_zic = None
        lng_zic = None

        if isinstance(address, list):
            # address가 배열인 경우 처리
            address = address[0]
            lat_zic = address.get('lat')
            lng_zic = address.get('lng')
            name = address.get('title')
            addr_info = {
                "name": name,
                "lat": lat_zic,
                "lng": lng_zic,
            }
            # 처리할 작업 수행
        elif isinstance(address, str):
            # address가 문자열인 경우 처리
            addr_lat, addr_lng = get_lat_lng_from_address(address)
            addr_info = {
                "name": 000,
                "lat": addr_lat,
                "lng": addr_lng,
            }
        else:
            pass
        selected = json.loads(selected)
        score = score_accesibility(address, selected, lat_zic=lat_zic, lng_zic=lng_zic)
        scorebox = {'score':score}
        info_store = serve_latlng(address, selected, lat_zic=lat_zic, lng_zic=lng_zic)
        if lat_zic == None and lng_zic == None:
            bus_data = get_bus_nearby(addr_lat, addr_lng)
        else:
            bus_data = get_bus_nearby(lat_zic, lng_zic)
        res = {
            'scorebox': scorebox,
            'info_store': info_store,
            'address_point': addr_info,
            'bus_data': bus_data,
        }
        return Response(res)


@api_view(['GET'])
def ZicbangServe(request):
    # 데이터를 처리하고 직렬화
    data = {'data': oneroom('아주대학교')}
    return Response(data)


class InfoView(APIView):
    def post(self, request):
        zicbang_ = False
        # POST 데이터를 JSON 형식으로 받아옵니다.
        data = request.data

        # 필요한 데이터 추출
        address = data.get("address")
        selected = data.get("selected", [])
        lat_zic = None
        lng_zic = None

        if isinstance(address, list):
            # address가 배열인 경우 처리
            address = address[0]
            lat_zic = address.get('lat')
            lng_zic = address.get('lng')
            name = address.get('title')
            addr_info = {
                "name": name,
                "lat": lat_zic,
                "lng": lng_zic,
            }
            zicbang_ = True
            # 처리할 작업 수행
        elif isinstance(address, str):
            # address가 문자열인 경우 처리
            addr_lat, addr_lng = get_lat_lng_from_address(address)
            addr_info = {
                "name": 000,
                "lat": addr_lat,
                "lng": addr_lng,
            }
        else:
            pass
        selected = json.loads(selected)
        score = score_accesibility(address, selected, lat_zic=lat_zic, lng_zic=lng_zic)
        scorebox = {'score':score}
        info_store = serve_latlng(address, selected, lat_zic=lat_zic, lng_zic=lng_zic)
        if lat_zic == None and lng_zic == None:
            bus_data = get_bus_nearby(addr_lat, addr_lng)
        else:
            bus_data = get_bus_nearby(lat_zic, lng_zic)
        oneroom_data = oneroom_df('아주대학교')
        
        columns_to_convert = ['deposit', 'rent', 'area_p', 'manage_cost']
        oneroom_data[columns_to_convert] = oneroom_data[columns_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0).astype(float)
        scaler = MinMaxScaler()
        features = scaler.fit_transform(oneroom_data[columns_to_convert])

        # 모델 불러오기
        loaded_model = joblib.load('./api/kmeans_model_final_++.pkl')
        predictions = loaded_model.predict(features)
        # 모델 입히기
        oneroom_data = oneroom_data.assign(cluster=predictions)


        if zicbang_:
            # 특정 조건에 맞는 행 필터링
            oneroom_data['my'] = (oneroom_data['title'] == name)
            oneroom_data_json = oneroom_data.to_json(orient='records', force_ascii=False)
        
        res = {
            'scorebox': scorebox,
            'info_store': info_store,
            'address_point': addr_info,
            'bus_data': bus_data,
            'oneroom_data_cluster':oneroom_data_json,
            'my_data': "why"
        }
        return Response(res)