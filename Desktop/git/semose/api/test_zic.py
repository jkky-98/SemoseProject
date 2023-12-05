from pyproj import Proj, transform

def search_zic_x,y(urlX, urlY):
    epsg_5181 = Proj(init='epsg:5181')
    epsg_4326 = Proj(init='epsg:4326')  # WGS84 좌표

    urlX=urlX * 0.4
    urlY=urlY * 0.4

    # 카카오맵 좌표를 WGS84로 변환
    longitude, latitude = transform(epsg_5181, epsg_4326, urlX, urlY)

    return longitude, latitude


print(f"변환된 위도: {latitude}, 변환된 경도: {longitude}")