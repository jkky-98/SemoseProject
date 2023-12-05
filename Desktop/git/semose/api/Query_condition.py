# 조건에 해당하는 데이터프레임 반환

# ----------- 예시 조건 ------------ 
# 클라이언트로부터 주소를 받음
# 클라이언트가 스타벅스, 맥도날드, 올리브영, 크린토피아를 선택함
import pandas as pd
import mysql.connector
import math
from .dis_min import haversine, change_min
from .change import get_lat_lng_from_address
from .query_dict import query_dict
import numpy as np
import json

def distance_weight(distance):
    sector_1 = 1
    sector_2 = 0.7
    sector_3 = 0.1
    sector_4 = 0

    m_1 = 1
    m_2 = 10
    m_3 = 20
    m_4 = 30

    if distance <= m_1:
        return sector_1
    elif distance <= m_2:
        # 제곱 또는 세제곱 등 다항식으로 변경하여 가파르게 설정할 수 있습니다.
        return sector_1 + ((distance - m_1) / (m_2 - m_1)) * (sector_2 - sector_1)
    elif distance <= m_3:
        return sector_2 + ((distance - m_2) / (m_3 - m_2)) * (sector_3 - sector_2)
    elif distance <= m_4:
        return sector_3 + ((distance - m_3) / (m_4 - m_3)) * (sector_4 - sector_3)
    else:
        return 0
    
        

class QuerySemose:
    def __init__(self, host="jkkyui-MacBookPro.local", user="root", password="apdlvmf4@@", database="Semose_DB"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tabel_name = "places"
    def get_info_condition(self, client_address, client_condition, lat_zic=None, lng_zic=None):
        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # SQL 쿼리를 사용하여 데이터를 데이터프레임으로 가져옵니다.
        # 동적 쿼리 생성
        query_key = client_condition[0]
        query = query_dict[query_key]

        # 거리 계산해서 distance에 반영
        df = pd.read_sql(query, connection)
        # 클라이언트로부터 입력받은 주소 위경도로 변환
        if lat_zic == None and lng_zic == None:
            lat, lng = get_lat_lng_from_address(client_address)
        else:
            lat, lng = lat_zic, lng_zic

        # 거리 계산
        try:
            df["distance"] = df.apply(lambda x: change_min(lat, lng, x["y"], x["x"]), axis=1)
        except:
            print('query error : data 추출 불가 검색어 확인 요망')

        df = df.sort_values(by=["distance"])

        connection.close()
        # 거리가 가까운 순으로 5개만 반환
        return df
    
    def get_one_info(self, client_address, shop_name, minutes, first=False ,lat_zic=None, lng_zic=None):
        try:
            df = self.get_info_condition(client_address, [shop_name], lat_zic, lng_zic)
        except:
            print("df를 불러오는 것에 실패했습니다")
        df = df[df['distance'] <= minutes]
        if first:
            df = df.iloc[0]
        return df
    
    def get_latlng(self, client_address, shop_name, minutes, first=False, lat_zic=None, lng_zic=None):
        df = self.get_info_condition(client_address, [shop_name], lat_zic, lng_zic)
        df = df[df['distance'] <= minutes]
        if first:
            df = df.iloc[0]


        lat = df.y # 위도

        lng = df.x # 경도

        name = df.place_name # 지점 이름

        address = df.road_address_name # 주소
        
        try:
            distance = round(df.distance,2) # 걸리는 시간
        except:
            distance = None

        phone = df.phone

        place_url = df.place_url


        return lat, lng, name, address, distance, phone, place_url
    
    def how_many_place(self, address, shop_lst, minutes=10, lat_zic=None, lng_zic=None):

        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        tmp_dict = {}
        # SQL 쿼리를 사용하여 데이터를 데이터프레임으로 가져옵니다.
        # 동적 쿼리 생성
        for i in range(len(shop_lst)):
            query_key = shop_lst[i]
            query = query_dict[query_key]
            # 거리 계산해서 distance에 반영
            df = pd.read_sql(query, connection)
            # 클라이언트로부터 입력받은 주소 위경도로 변환
            if lat_zic == None and lng_zic == None:
                lat, lng = get_lat_lng_from_address(address)
            else:
                lat, lng = lat_zic, lng_zic

            # 거리 계산
            try:
                df["distance"] = df.apply(lambda x: change_min(lat, lng, x["y"], x["x"]), axis=1)
            except:
                print('query error : data 추출 불가 검색어 확인 요망')

            df = df.sort_values(by=["distance"])
            df = df[df['distance'] <= minutes]
            tmp_dict[shop_lst[i]] = len(df)
            
        return tmp_dict



        
def score_accesibility(address, shop_lst, lat_zic=None, lng_zic=None):
    weights = np.array([])
    find = QuerySemose()

    for i in shop_lst:
        tmp = find.get_one_info(address, i, 10000, True, lat_zic, lng_zic)
        tmp['weight'] = distance_weight(tmp['distance'])
        weights = np.append(weights, tmp['weight'])
    
    # NumPy 배열을 사용하여 평균 계산
    average_weight = np.mean(weights)

    # 점수
    score = round(average_weight * 100, 2)
    return score

def serve_latlng(address, shop_lst, lat_zic=None, lng_zic=None):
    find = QuerySemose()
    shop_data = []

    for i in shop_lst:
        lat, lng, name, address_, distance, phone, place_url = find.get_latlng(address, i, 10000, True, lat_zic, lng_zic)

        shop_info = {
            "name": name,
            "lat": lat,
            "lng": lng,
            "address": address_,
            "distance": distance,
            "phone": phone,
            "place_url": place_url
        }
        shop_data.append(shop_info)

    # JSON 형식으로 변환
    json_data = json.dumps(shop_data, ensure_ascii=False)

    return json_data

            
        
