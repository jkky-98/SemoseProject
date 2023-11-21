<template>
  <div>
    <h2 class="map-title">Semose Kakao Map~!</h2>
    <div id="map"></div>
    <button @click="calculateDistance">Calculate Distance</button>
  </div>
  <div>
   <p>fdasfasgf : {{parentData}}</p>
  </div>
</template>

<script>

export default {
  name: "KakaoMap",
  data() {
    return {
      scorebox: null,
      address: { name: 'my house', lat: 37.0781534, lng: 127.0427976 },
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
  props: {
    parentData: {
      type: Object,
      required: true
    }
  },
  mounted() {

    if (window.kakao && window.kakao.maps) {
      this.loadMap();
    } else {
      this.loadScript();
    }

  },
  methods: {
  
    loadScript() {
      const script = document.createElement("script");
      script.src =
        "https://dapi.kakao.com/v2/maps/sdk.js?appkey=14d78dd0b00ee306c710756383b6e3e7&autoload=false&libraries=services,clusterer,drawing";
      script.type = 'text/javascript';
      script.onload = () => window.kakao.maps.load(() => this.loadMap());
      document.head.appendChild(script);
    },
    loadMap() {
      const container = document.getElementById("map");

      // 맵 기본위치 설정 및 사이즐 
      const options = {
        center: new window.kakao.maps.LatLng(this.parentData.address_latlng.lat, this.parentData.address_latlng.lng),
        level: 3,
      };
      // 기본 맵 띄우기
      this.map = new window.kakao.maps.Map(container, options);

      this.$nextTick(() => {
            this.addSetFull(this.parentData.info_store, 
            this.parentData.address_latlng, 
            this.parentData.bus);
          });
      // 맵 추가 기능
    },

    addMarker(lat, lng) {
            // 마커가 표시될 위치입니다 
      var markerPosition  = new window.kakao.maps.LatLng(lat, lng); 

      // 마커를 생성합니다
      var marker = new window.kakao.maps.Marker({
          position: markerPosition,
          clickable: true
      });

      // 마커가 지도 위에 표시되도록 설정합니다
      marker.setMap(this.map);
    },

    addLine(address, lat_end, lng_end, color='#FFAE00') {
      var linePath = [
      new window.kakao.maps.LatLng(address.lat, address.lng),
      new window.kakao.maps.LatLng(lat_end, lng_end)
      ]
        // 지도에 표시할 선을 생성합니다
      var polyline = new window.kakao.maps.Polyline({
          path: linePath, // 선을 구성하는 좌표배열 입니다
          strokeWeight: 5, // 선의 두께 입니다
          strokeColor: color, // 선의 색깔입니다
          strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
          strokeStyle: 'solid' // 선의 스타일입니다
      });
      polyline.setMap(this.map);  
    },
    customOverlay(lat, lng, name, distance) {
      var iwContent = name+distance, // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
          iwPosition = new window.kakao.maps.LatLng(lat, lng), //인포윈도우 표시 위치입니다
          iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

      // 인포윈도우를 생성하고 지도에 표시합니다
      new window.kakao.maps.InfoWindow({
          map: this.map, // 인포윈도우가 표시될 지도
          position : iwPosition, 
          content : iwContent,
          removable : iwRemoveable
      });
    },
    customOverlay_house(lat, lng) {
      var iwContent = "my house SCORE : "+ this.parentData.scorebox.score, // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
          iwPosition = new window.kakao.maps.LatLng(lat, lng), //인포윈도우 표시 위치입니다
          iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

      // 인포윈도우를 생성하고 지도에 표시합니다
      new window.kakao.maps.InfoWindow({
          map: this.map, // 인포윈도우가 표시될 지도
          position : iwPosition, 
          content : iwContent,
          removable : iwRemoveable
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
      this.addMarker(address.lat, address.lng)
      this.customOverlay_house(address.lat, address.lng)
      // About stores point
      stores.forEach((store) => {
        const {name, lat, lng, distance} = store
        this.addMarker(lat, lng);
        this.addLine(address, lat, lng);
        this.customOverlay(lat, lng, name, distance);
      });
      // About bus point
      bus.forEach((bus) => {
        const {name, lat, lng, distance} = bus
        this.addMarker(lat, lng);
        this.addLine(address, lat, lng, '#29B6F6');
        this.customOverlay(lat, lng, name, distance);
      });
    },

    reMap() {
      console.log("SUCCESS REMAP");
      this.loadMap();
      
    },

  },
};

</script>

<style>
#map {
  width: 1300px; /* 변경할 너비 값 */
  height: 800px; /* 변경할 높이 값 */
  margin: auto; /* 가운데 정렬을 위한 margin 속성 */
  display: block; /* 블록 요소로 표시하여 가로폭 전체를 차지하도록 설정 */
}
.map-title {
  color: white;
}
</style>

