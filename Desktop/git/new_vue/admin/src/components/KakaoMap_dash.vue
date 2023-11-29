<template>
  <div class="map-container">
    <div id="map"></div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "KakaoMap_dash",
  data() {
    return {
      scorebox: null,
      address: { name: "my house", lat: 37.0781534, lng: 127.0427976 },
      stores: [
        { name: "Starbucks", lat: 37.2796352, lng: 127.043346 },
        { name: "Burger King", lat: 37.2745815, lng: 127.045215 },
        { name: "Daiso", lat: 37.2754895, lng: 127.0423236 },
      ],
      map: null,
    };
  },
  created() {
    this.loadScript();
  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.loadMap();
    } else {
      this.loadScript();
    }
  },
  computed: {
    ...mapState({
      dash_zickbang_source: (state) => state.dash_zickbang_source,
    }),
  },
  methods: {
    loadScript() {
      const script = document.createElement("script");
      script.src =
        "https://dapi.kakao.com/v2/maps/sdk.js?appkey=14d78dd0b00ee306c710756383b6e3e7&autoload=false&libraries=services,clusterer,drawing";
      script.type = "text/javascript";
      script.onload = () => window.kakao.maps.load(() => this.loadMap());
      document.head.appendChild(script);
    },
    loadMap() {
      const container = document.getElementById("map");

      // 맵 기본위치 설정 및 사이즐
      const options = {
        center: new window.kakao.maps.LatLng(37.282972, 127.045545),
        level: 3,
      };
      // 기본 맵 띄우기
      this.map = new window.kakao.maps.Map(container, options);
    },
    reLoadMap(data) {
      const container = document.getElementById("map");
      // 맵 기본위치 설정 및 사이즈
      const options = {
        center: new window.kakao.maps.LatLng(37.282972, 127.045545),
        level: 3,
      };
      this.map = new window.kakao.maps.Map(container, options);
      data.forEach((data) => {
        const {
          lat,
          lng,
          distance,
          name,
          title,
          area_p,
          deposit,
          floor,
          rent,
          manage_cost,
          sales_type,
        } = data;
        console.log(
          lat,
          lng,
          distance,
          name,
          title,
          area_p,
          deposit,
          floor,
          rent,
          manage_cost,
          sales_type
        );
        this.addMarker(lat, lng);
      });
    },

    addMarker(lat, lng) {
      // 마커가 표시될 위치입니다
      var markerPosition = new window.kakao.maps.LatLng(lat, lng);
      var imageSrc = "@/assets/free-icon-location-pin-8637632.png";
      var imageSize = new window.kakao.maps.Size(24, 35);
      var imageOption = { offset: new window.kakao.maps.Point(24, 35) };

      // 마커를 생성합니다
      var markerImage = new window.kakao.maps.MarkerImage(
        imageSrc,
        imageSize,
        imageOption
      );
      var marker = new window.kakao.maps.Marker({
        position: markerPosition,
        clickable: true,
        image: markerImage,
      });

      // 마커가 지도 위에 표시되도록 설정합니다
      marker.setMap(this.map);

      // 마커 클릭 이벤트 리스너를 등록합니다
      window.kakao.maps.event.addListener(marker, "click", function () {
        // 마커의 이미지를 변경합니다 (새로운 이미지로 교체하여 마커의 색상을 변경)
        var newImageSrc = "@/assets/free-icon-location-pointer-2098567.png";
        var newImageSize = new window.kakao.maps.Size(24, 35);
        var newImageOption = { offset: new window.kakao.maps.Point(24, 35) };
        var newMarkerImage = new window.kakao.maps.MarkerImage(
          newImageSrc,
          newImageSize,
          newImageOption
        );

        marker.setImage(newMarkerImage); // 마커의 이미지를 변경합니다
      });
    },
    // 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
    optionZoomControl() {
      var zoomControl = new window.kakao.maps.ZoomControl();
      this.map.addControl(zoomControl, window.kakao.maps.ControlPosition.RIGHT);
    },
    optionTopographical() {
      this.map.addOverlayMapTypeId(window.kakao.maps.MapTypeId.TERRAIN);
    },
  },
};
</script>

<style>
#map {
  width: 1200px; /* 지도의 크기 지정 */
  height: 800px;
  margin: auto; /* 가운데 정렬을 위한 margin 속성 */
  display: block; /* 블록 요소로 표시하여 가로폭 전체를 차지하도록 설정 */
}
.map-title {
  color: white;
}

.map-container {
  background-color: #272727; /* 회색 배경색 설정 */
  border: 1px solid #272727; /* 테두리 설정 */
  padding: 20px; /* 위 아래 여백 설정 */
  margin-top: 20px; /* 위쪽 간격 설정 */
  margin-bottom: 20px; /* 아래쪽 간격 설정 */
  border-radius: 10px; /* 모서리를 둥글게 설정 */
  /* 원하는 스타일을 추가할 수 있습니다. */
}
.over-wrap {
  position: absolute;
  left: 0;
  bottom: 20px;
  width: auto;
  height: 66px;
  margin-left: -48px;
  text-align: left;
  overflow: hidden;
  font-size: 4px;
  font-family: "Malgun Gothic", dotum, "돋움", sans-serif;
  line-height: 1.5;
}
.over-wrap .over-info {
  width: 120px;
  max-height: 60px;
  overflow: auto;
  height: 60px;
  border-radius: 5px;
  border-bottom: 1px solid #ccc;
  border-right: 1px solid #ccc;
  overflow: hidden;
  background: #fff;
  padding: 0;
}
.over-info .over-title {
  display: flex; /* title을 flex로 설정하여 x 버튼이 항상 첫번째 줄에 위치하도록 합니다. */
  align-items: center; /* x 버튼을 가운데 정렬합니다. */
  padding: 2px 0 0 3px;
  width: 120px; /* title의 width를 고정값으로 설정합니다. */
  height: auto;
  background: #eee;
  border-bottom: 1px solid #ddd;
  font-size: 10px;
  font-weight: bold;
  word-break: break-word; /* 긴 단어가 다음 줄로 넘어가도록 설정합니다. */
}
.over-info .over-close {
  position: absolute;
  top: 0px;
  right: 5px;
  color: #888;
  width: 16px;
  height: 16px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/overlay_close.png");
}
.over-info .over-body {
  position: relative;
  overflow: hidden;
}
.over-info .over-desc {
  position: relative;
  margin: 1px 0 0 5px;
  height: 38px;
}
.over-desc .over-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 8px;
}
.over-desc .over-jibun {
  font-size: 8px;
  color: #888;
  margin-top: -1px;
}
.over-info .over-img {
  position: absolute;
  top: 3px;
  left: 2px;
  width: 24px;
  height: 24px;
  border: 1px solid #ddd;
  color: #888;
  overflow: hidden;
}
.over-info:after {
  content: "";
  position: absolute;
  margin-left: -4px;
  left: 50%;
  bottom: 0;
  width: 7px;
  height: 6px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/vertex_white.png");
}
.over-info .over-link {
  color: #5085bb;
  font-size: 8px;
}
/* bus style */
.bus-wrap {
  position: absolute;
  left: 0;
  bottom: 20px;
  width: auto;
  height: 66px;
  margin-left: -48px;
  text-align: left;
  overflow: hidden;
  font-size: 4px;
  font-family: "Malgun Gothic", dotum, "돋움", sans-serif;
  line-height: 1.5;
}
.bus-wrap .bus-info {
  width: 120px;
  max-height: 60px;
  overflow: auto;
  height: 60px;
  border-radius: 5px;
  border-bottom: 1px solid #ccc;
  border-right: 1px solid #ccc;
  overflow: hidden;
  background: #fff;
  padding: 0;
}
.bus-info .bus-title {
  display: flex; /* title을 flex로 설정하여 x 버튼이 항상 첫번째 줄에 위치하도록 합니다. */
  align-items: center; /* x 버튼을 가운데 정렬합니다. */
  padding: 2px 0 0 3px;
  width: 120px; /* title의 width를 고정값으로 설정합니다. */
  height: auto;
  background: #87ceeb;
  border-bottom: 1px solid #ddd;
  font-size: 10px;
  font-weight: bold;
  word-break: break-word; /* 긴 단어가 다음 줄로 넘어가도록 설정합니다. */
}
.bus-info .bus-close {
  position: absolute;
  top: 0px;
  right: 5px;
  color: #888;
  width: 16px;
  height: 16px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/overlay_close.png");
}
.bus-info .bus-body {
  position: relative;
  overflow: hidden;
}
.bus-info .bus-desc {
  position: relative;
  margin: 1px 0 0 5px;
  height: 38px;
}
.bus-desc .bus-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 8px;
}
.bus-desc .bus-jibun {
  font-size: 8px;
  color: #888;
  margin-top: -1px;
}
.bus-info .bus-img {
  position: absolute;
  top: 3px;
  left: 2px;
  width: 24px;
  height: 24px;
  border: 1px solid #ddd;
  color: #888;
  overflow: hidden;
}
.bus-info:after {
  content: "";
  position: absolute;
  margin-left: -4px;
  left: 50%;
  bottom: 0;
  width: 7px;
  height: 6px;
  background: url("https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/vertex_white.png");
}
.bus-info .bus-link {
  color: #5085bb;
  font-size: 8px;
}
</style>
