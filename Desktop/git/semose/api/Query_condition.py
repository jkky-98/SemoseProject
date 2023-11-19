# 조건에 해당하는 데이터프레임 반환

# ----------- 예시 조건 ------------ 
# 클라이언트로부터 주소를 받음
# 클라이언트가 스타벅스, 맥도날드, 올리브영, 크린토피아를 선택함
import pandas as pd
import mysql.connector
import math
from dis_min import haversine, change_min
from change import get_lat_lng_from_address
import numpy as np

def distance_weight(distance):
    sector_1 = 1
    sector_2 = 0.7
    sector_3 = 0.2
    sector_4 = 0

    m_1 = 3
    m_2 = 10
    m_3 = 15
    m_4 = 30

    if distance <= m_1:
        return sector_1
    if distance <= m_2:
        return sector_1 + (distance - m_1) * (sector_2 - sector_1) / (m_2 - m_1)
    if distance <= m_3:
        return sector_2 + (distance - m_2) * (sector_3 - sector_2) / (m_3 -  m_2)
    if distance <= m_4:
        return max(sector_3 + (distance - m_3) * (sector_4 - sector_3) / (m_4 - m_3), 0)
    
        

class QuerySemose:
    def __init__(self, host="jkkyui-MacBookPro.local", user="root", password="apdlvmf4@@", database="Semose_DB"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tabel_name = "places"
    def get_info_condition(self, client_address, client_condition):
        # MySQL 서버에 연결
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # SQL 쿼리를 사용하여 데이터를 데이터프레임으로 가져옵니다.
        # 동적 쿼리 생성
        query_conditions = " OR ".join([f"place_name LIKE '%{item}%'" for item in client_condition])
        query = f"SELECT * FROM {self.tabel_name} WHERE {query_conditions}"

        # 거리 계산해서 distance에 반영
        df = pd.read_sql(query, connection)
        # 클라이언트로부터 입력받은 주소 위경도로 변환
        lat, lng = get_lat_lng_from_address(client_address)

        # 거리 계산
        try:
            df["distance"] = df.apply(lambda x: change_min(lat, lng, x["y"], x["x"]), axis=1)
        except:
            print('query error : data 추출 불가 검색어 확인 요망')

        df = df.sort_values(by=["distance"])

        connection.close()
        # 거리가 가까운 순으로 5개만 반환
        return df
    
    def get_one_info(self, client_address, shop_name, minutes, first=False):
        df = self.get_info_condition(client_address, [shop_name])
        df = df[['place_name','distance']]
        df = df[df['distance'] <= minutes]
        if first:
            df = df.iloc[0]

        return df
        
def score_accesibility(address, shop_lst):
    weights = np.array([])
    find = QuerySemose()

    for i in shop_lst:
        tmp = find.get_one_info(address, i, 10000, True)
        tmp['weight'] = distance_weight(tmp['distance'])
        weights = np.append(weights, tmp['weight'])
    # NumPy 배열을 사용하여 평균 계산
    average_weight = np.mean(weights)

    # 점수
    score = round(average_weight * 100, 2)
    return score

print(score_accesibility('경기 수원시 팔달구 인계동 374-7', ['스타벅스', '맥도날드', '편의점']))