# get bus that is nearby target address in Suwon
import pandas as pd
import pymysql
from .dis_min import change_min

def get_bus_nearby(lat, lng, 
                   host="jkkyui-MacBookPro.local", 
                   user="root", 
                   password="apdlvmf4@@", 
                   database="Semose_DB"):

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # SQL 쿼리 실행하여 데이터프레임으로 받아오기
    query = "SELECT * FROM bus"
    df = pd.read_sql_query(query, connection)

    df["distance"] = df.apply(lambda x: change_min(lat, lng, x["lat"], x["lng"]), axis=1)
    df = df.sort_values(by='distance')
    df = df.iloc[:2]

    json_data = df.to_json(orient='records', force_ascii=False)
    return json_data
