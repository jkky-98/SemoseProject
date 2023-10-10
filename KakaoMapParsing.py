import requests
import mysql.connector

class CrawlerPlaceKakao:
    def __init__(self, host, user, password, database, auth_key):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.auth_key = auth_key


    
    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
    
    def get_cursor(self, connection):
        return connection.cursor(prepared=True)
    
    def close_connection(self, cursor, connection):
        cursor.close()
        connection.close()
    
    def get_places(self, searching):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
        headers = {
            "Authorization": self.auth_key
        }
        data = requests.get(url, headers = headers).json()['documents']
        print(data)
        connection = self.get_connection()
        cursor = self.get_cursor(connection)

        for entry in data:
            for key in entry:
                if entry[key] == '':
                    entry[key] = None  # 빈 문자열을 None으로 대체
            query = """
                    INSERT IGNORE INTO places (address_name, category_group_code, category_group_name, category_name, 
                    distance, id, phone, place_name, place_url, road_address_name, x, y)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            values = (
            entry['address_name'],
            entry['category_group_code'],
            entry['category_group_name'],
            entry['category_name'],
            entry['distance'],
            entry['id'],
            entry['phone'],
            entry['place_name'],
            entry['place_url'],
            entry['road_address_name'],
            entry['x'],
            entry['y']
            )


            cursor.execute(query, values)
            connection.commit()

    # 연결 종료
        self.close_connection(cursor, connection)

test = CrawlerPlaceKakao(host="jkkyui-MacBookPro.local",
                         user="root",
                         password="apdlvmf4@@",
                         database="Semose_DB",
                         auth_key="KakaoAK dfe9007a5ea05518f9df2ea00e395d43")
test.get_places('인계동374-7 스타벅스')

