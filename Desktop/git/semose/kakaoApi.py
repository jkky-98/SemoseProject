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


list_facility = [
    '편의점', '대형마트', '카페', '약국', '세탁소', '부동산', '인쇄', 'PC방', 
    '내과', '한의원', '우체국', '올리브영', '영화관', '헬스장', '필라테스', '코인노래방', '공원',
    '맥도날드', '롯데리아', '버거킹', '베스킨라빈스', '파리바게뜨', '스타벅스', '메가커피', '컴포즈커피', '빽다방', '이디야커피', '투썸플레이스'
]


        # 편의점: query = "SELECT * FROM places WHERE category_group_code = 'CS2';"
        # 대형마트: query = "SELECT * FROM places WHERE category_group_code = 'MT1';"
        # 아주대학교: query = "SELECT * FROM places WHERE place_name = '아주대학교';"
        # 카페: query = "SELECT * FROM places WHERE category_group_code = 'CE7';"
        # 약국 query= "SELECT * FROM places WHERE category_group_code = 'PM9';"
        # 세탁소 query = "SELECT * FROM places WHERE (place_name LIKE '%크린토피아%') OR (place_name LIKE '%빨래%') OR (place_name LIKE '%세탁소%');"
        
        # 부동산 query = "SELECT * FROM places WHERE category_group_code = 'AG2';"
        # 인쇄 query = "SELECT * FROM places WHERE category_name LIKE '%인쇄%';"
        # PC방 query = "SELECT * FROM places WHERE category_name LIKE '%PC방%';"
        # 내과 query = "SELECT * FROM places WHERE category_name LIKE '%내과%';"
        # 한의원 query = "SELECT * FROM places WHERE category_name LIKE '%한의원%';"
        # 우체국 query = "SELECT * FROM places WHERE category_name LIKE '%우체국%';"
        # 올리브영 query = "SELECT * FROM places WHERE category_name LIKE '%올리브영%';"
        # 영화관 query = "SELECT * FROM places WHERE category_name LIKE '%영화관%';"
        # 헬스장 query = "SELECT * FROM places WHERE category_name LIKE '%헬스클럽%';"
        # 필라테스 query = "SELECT * FROM places WHERE category_name LIKE '%필라테스%';"
        # 코인노래방 query = "SELECT * FROM places WHERE category_name LIKE '%코인노래방%';"
        # 공원 query = "SELECT * FROM places WHERE category_name LIKE '%도시근린공원%';"
        # 맥도날드 query = "SELECT * FROM places WHERE category_name LIKE '%맥도날드%';"
        # 롯데리아 query = "SELECT * FROM places WHERE category_name LIKE '%롯데리아%';"
        # 버거킹 query = "SELECT * FROM places WHERE category_name LIKE '%버거킹%';"
        # 베스킨라빈스 query = "SELECT * FROM places WHERE category_name LIKE '%배스킨라빈스%';"
        # 파리바게뜨 query = "SELECT * FROM places WHERE category_name LIKE '%파리바게뜨%';"
        # 스타벅스 query = "SELECT * FROM places WHERE category_name LIKE '%스타벅스%';"
        # 메가커피 query = "SELECT * FROM places WHERE category_name LIKE '%메가MGC커피%';"
        # 컴포즈커피 query = "SELECT * FROM places WHERE category_name LIKE '%컴포즈커피%';"
        # 빽다방 query = "SELECT * FROM places WHERE category_name LIKE '%빽다방%';"
        # 이디야커피 query = "SELECT * FROM places WHERE category_name LIKE '%이디야커피%';"
        # 투썸플레이스 query = "SELECT * FROM places WHERE category_name LIKE '%투썸플레이스%';"

lst_addr = ['팔달구 창룡대로 44', '팔달구 팔달문로75번길 84' ,'팔달문로153번길 9-11', '팔달구 월드컵로 256',
            '팔달구 창룡대로103번길 20', '팔달구 경수대로692번길 28-14', '팔달구 월드컵로321번길 17',
            '장안구 월드컵로 428-1','장안구 창룡대로 175','팔달구 월드컵로 336',
            '장안구 창훈로 57-11','팔달구 창룡대로210번길 13',
            '영통구 광교산로 154-42','영통구 창룡대로 260',
            '영통구 광교산로 154-42','영통구 창룡대로256번길 14','팔달구 월드컵로 310',
            '영통구 대학3로4번길 36','영통구 광교로 147','영통구 광교로 105',
            '영통구 대학4로 33','영통구 이의동 832-4', '영통구 도청로 103',
            '영통구 창룡대로 442','영통구 센트럴파크로127번길 83','영통구 센트럴타운로 85','영통구 에듀타운로 65',
            '영통구 센트럴파크로 100','영통구 센트럴타운로 55','영통구 도청로 65',
            '영통구 센트럴파크로 34', '경기 수원시 영통구 도청로 65',
            '영통구 법조로 38','영통구 도청로17번길 23',
            '영통구 광교호수로 139', '영통구 광교호수공원로 277','영통구 혜령로 17',
            '영통구 광교호수공원로 277', '영통구 광교중앙로 55',
            '영통구 광교호수공원로 155', '영통구 광교호수공원로 80 앨리웨이',
            '영통구 광교중앙로 30','영통구 중부대로392번길 21',
            '영통구 월드컵로87번길 16', '영통구 광교중앙로25번길 77',
            '영통구 매영로 110', '영통구 매봉로35번길 23-18','영통구 동수원로551번길 21',
            '영통구 월드컵로179번길 32-3', '영통구 동수원로513번길 11', '영통구 매영로35번길 25','영통구 매원로11번길 8-16',
            '영통구 인계로 239','영통구 동수원로 482','영통구 매여울로61번길 28', '수원시 팔달구 아주로 17',
            '영통구 인계로189번길 14', '영통구 권광로260번길 36', '영통구 중부대로246번길 40-15','팔달구 아주로27번길 35',
            '영통구 권광로290번길 34-11', '팔달구 권광로260번길 20','영통구 인계로 165',
            '팔달구 인계로 123','팔달구 권광로 293','팔달구 중부대로 194',
            '팔달구 권광로364번길 7-2','팔달구 중부대로 165','팔달구 경수대로 568','팔달구 장다리로 269',
            '팔달구 지동 349-1','팔달구 중부대로125번길 15-19', '팔달구 권광로 373','팔달구 중부대로223번길 102',
            ]

# for addr in lst_addr:
#     for facility in list_facility:
#         test.get_places(addr + ' ' + facility)

test.get_places('아주대학교')
