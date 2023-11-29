<template>
  <div class="map-container">
    <v-card-text class="text-center justify-center font-weight-bold text-h4"
      >MAP INFO</v-card-text
    >
    <div id="map"></div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "KakaoMap",
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
      receivedData: "receivedData",
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
    reLoadMap() {
      const container = document.getElementById("map");
      // 맵 기본위치 설정 및 사이즈
      const options = {
        center: new window.kakao.maps.LatLng(
          this.receivedData.address_latlng.lat,
          this.receivedData.address_latlng.lng
        ),
        level: 3,
      };
      this.map = new window.kakao.maps.Map(container, options);
      this.$nextTick(() => {
        this.addSetFull(
          this.receivedData.info_store,
          this.receivedData.address_latlng,
          this.receivedData.bus
        );
      });
    },

    addMarker(lat, lng) {
      // 마커가 표시될 위치입니다
      var markerPosition = new window.kakao.maps.LatLng(lat, lng);

      // 마커를 생성합니다
      var marker = new window.kakao.maps.Marker({
        position: markerPosition,
        clickable: true,
      });

      // 마커가 지도 위에 표시되도록 설정합니다
      marker.setMap(this.map);
    },

    addLine(address, lat_end, lng_end, color = "#FFAE00") {
      var linePath = [
        new window.kakao.maps.LatLng(address.lat, address.lng),
        new window.kakao.maps.LatLng(lat_end, lng_end),
      ];
      // 지도에 표시할 선을 생성합니다
      var polyline = new window.kakao.maps.Polyline({
        path: linePath, // 선을 구성하는 좌표배열 입니다
        strokeWeight: 5, // 선의 두께 입니다
        strokeColor: color, // 선의 색깔입니다
        strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        strokeStyle: "solid", // 선의 스타일입니다
      });
      polyline.setMap(this.map);
    },
    customOverlay_house(lat, lng) {
      var iwContent = "당신의 세권 점수 : " + this.receivedData.scorebox.score, // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
        iwPosition = new window.kakao.maps.LatLng(lat, lng), //인포윈도우 표시 위치입니다
        iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

      // 인포윈도우를 생성하고 지도에 표시합니다
      new window.kakao.maps.InfoWindow({
        map: this.map, // 인포윈도우가 표시될 지도
        position: iwPosition,
        content: iwContent,
        removable: iwRemoveable,
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
    addSetFull(stores, address, bus) {
      // Setting Option
      this.optionZoomControl();
      this.optionTopographical();
      // About address point
      this.addMarker(address.lat, address.lng);
      this.customOverlay_house(address.lat, address.lng);
      // About stores point
      stores.forEach((store) => {
        const { name, lat, lng, distance, phone, place_url } = store;
        this.addMarker(lat, lng);
        this.addLine(address, lat, lng);
        this.customOverlay(lat, lng, distance, name, phone, place_url);
      });
      // About bus point
      bus.forEach((bus) => {
        const { lat, lng, distance, name } = bus;
        this.addMarker(lat, lng);
        this.addLine(address, lat, lng, "#29B6F6");
        this.customOverlayBUS(lat, lng, distance, name);
      });
    },

    customOverlay(lat, lng, distance, name, number, placeurl) {
      const content = document.createElement("div");
      content.className = "over-wrap";
      const chunks = [];
      for (let i = 0; i < name.length; i += 10) {
        chunks.push(name.substring(i, i + 10));
      }
      const modifiedName = chunks.join("<br>");
      content.innerHTML = `
      <div class="over-info">
        <div class="over-title">
          ${modifiedName}
          <div class="over-close" id="closeBtn" title="닫기" style="right: 5px"></div>
        </div>
        <div class="over-body">
          <div class="over-desc">
            <div class="over-ellipsis">${distance}분 거리</div>
            <div class="over-jibun ellipsis">${number}</div>
            <a href="${placeurl}" target="_blank" class="over-link">홈페이지 바로가기</a>
          </div>
        </div>
      </div>
      `;

      // X 버튼 추가
      const closeBtn = content.querySelector("#closeBtn");

      const overlay = new window.kakao.maps.CustomOverlay({
        map: this.map,
        content: content,
        position: new window.kakao.maps.LatLng(lat, lng),
        yAnchor: 1,
        clickable: true,
      });

      const onMouseDown = (e) => {
        if (e.preventDefault) {
          e.preventDefault();
        } else {
          e.returnValue = false;
        }

        const proj = this.map.getProjection();
        const overlayPos = overlay.getPosition();
        window.kakao.maps.event.preventMap();

        this.startX = e.clientX;
        this.startY = e.clientY;
        this.startOverlayPoint = proj.containerPointFromCoords(overlayPos);
        document.addEventListener("mousemove", onMouseMove);
      };

      const onMouseMove = (e) => {
        if (e.preventDefault) {
          e.preventDefault();
        } else {
          e.returnValue = false;
        }

        const proj = this.map.getProjection();
        const deltaX = this.startX - e.clientX;
        const deltaY = this.startY - e.clientY;
        const newPoint = new window.kakao.maps.Point(
          this.startOverlayPoint.x - deltaX,
          this.startOverlayPoint.y - deltaY
        );
        const newPos = proj.coordsFromContainerPoint(newPoint);
        overlay.setPosition(newPos);
      };

      const onMouseUp = () => {
        document.removeEventListener("mousemove", onMouseMove);
      };

      // X 버튼 클릭 시 오버레이 제거
      const onCloseClick = () => {
        overlay.setMap(null);
      };

      content.addEventListener("mousedown", onMouseDown);
      document.addEventListener("mouseup", onMouseUp);
      closeBtn.addEventListener("click", onCloseClick);
    },
    customOverlayBUS(lat, lng, distance, name) {
      const content = document.createElement("div");
      content.className = "bus-wrap";
      const chunks = [];
      for (let i = 0; i < name.length; i += 10) {
        chunks.push(name.substring(i, i + 10));
      }
      const modifiedName = chunks.join("<br>");
      content.innerHTML = `
      <div class="bus-info">
        <div class="bus-title">
          ${modifiedName} BUS STATION!!
          <div class="bus-close" id="closeBtn" title="닫기" style="right: 5px"></div>
        </div>
        <div class="bus-body">
          <div class="bus-desc">
            <div class="bus-ellipsis">${distance}분 거리</div>
          </div>
        </div>
      </div>
      `;

      // X 버튼 추가
      const closeBtn = content.querySelector("#closeBtn");

      const overlay = new window.kakao.maps.CustomOverlay({
        map: this.map,
        content: content,
        position: new window.kakao.maps.LatLng(lat, lng),
        yAnchor: 1,
        clickable: true,
      });

      const onMouseDown = (e) => {
        if (e.preventDefault) {
          e.preventDefault();
        } else {
          e.returnValue = false;
        }

        const proj = this.map.getProjection();
        const overlayPos = overlay.getPosition();
        window.kakao.maps.event.preventMap();

        this.startX = e.clientX;
        this.startY = e.clientY;
        this.startOverlayPoint = proj.containerPointFromCoords(overlayPos);
        document.addEventListener("mousemove", onMouseMove);
      };

      const onMouseMove = (e) => {
        if (e.preventDefault) {
          e.preventDefault();
        } else {
          e.returnValue = false;
        }

        const proj = this.map.getProjection();
        const deltaX = this.startX - e.clientX;
        const deltaY = this.startY - e.clientY;
        const newPoint = new window.kakao.maps.Point(
          this.startOverlayPoint.x - deltaX,
          this.startOverlayPoint.y - deltaY
        );
        const newPos = proj.coordsFromContainerPoint(newPoint);
        overlay.setPosition(newPos);
      };

      const onMouseUp = () => {
        document.removeEventListener("mousemove", onMouseMove);
      };

      // X 버튼 클릭 시 오버레이 제거
      const onCloseClick = () => {
        overlay.setMap(null);
      };

      content.addEventListener("mousedown", onMouseDown);
      document.addEventListener("mouseup", onMouseUp);
      closeBtn.addEventListener("click", onCloseClick);
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
