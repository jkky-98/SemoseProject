from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Place
from rest_framework.decorators import api_view
import pandas as pd
from dis_min import change_min
from change import get_lat_lng_from_address

@api_view(['GET'])
def get_info_one(request,
                client_address='팔달구 권광로 243 래미안노블클래스2단지아파트 202동', 
                shop_name='스타벅스',
                minutes=30,
                first=False):
    
    if request.method == 'GET':
        places = Place.objects.filter(place_name__icontains=shop_name)

    data = {
    'place_name': [place.place_name for place in places],
    'x': [place.x for place in places],
    'y': [place.y for place in places],
    }

    df = pd.DataFrame(data)

    lat, lng = get_lat_lng_from_address(client_address)

    # 거리 계산
    try:
        df["distance"] = df.apply(lambda x: change_min(lat, lng, x["y"], x["x"]), axis=1)
    except:
        print('query error : data 추출 불가 검색어 확인 요망')
    
    df = df.sort_values(by=["distance"])
    df = df[['place_name','distance']]
    df = df[df['distance'] <= minutes]

    if first:
        df = df.iloc[0]
    return df['place_name']

test = get_info_one()
print(test)
