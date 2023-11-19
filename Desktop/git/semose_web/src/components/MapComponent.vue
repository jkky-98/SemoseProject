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
      address: { name: "My house", lat: 37.2781534, lng: 127.0427976 },
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
    setData(data) {
          // 자식 컴포넌트의 데이터를 설정하는 메서드
          // 이 메서드는 부모 컴포넌트에서 호출됨
          this.receivedData = data;
        },

    addHouseMarker() {
      const { name, lat, lng } = this.address;
      this.addMarker(name, lat, lng);
    },
  
    loadScript() {
      const script = document.createElement("script");
      script.src =
        "https://dapi.kakao.com/v2/maps/sdk.js?appkey=14d78dd0b00ee306c710756383b6e3e7&autoload=false";
      script.onload = () => window.kakao.maps.load(() => this.loadMap());

      document.head.appendChild(script);
    },
    loadMap() {
      const container = document.getElementById("map");
      const options = {
        center: new window.kakao.maps.LatLng(37.282972, 127.045545),
        level: 3,
      };
      this.map = new window.kakao.maps.Map(container, options);
      this.loadStores(); // Move this line after initializing the map
      this.addHouseMarker();
    },
    loadStores() {
      this.parentData.info_store.forEach((store, index) => {
        const { name, lat, lng } = store;
        this.addMarker(name, lat, lng, index);
      });
    },
    addMarker(name, lat, lng, index) {
      const latlng = new window.kakao.maps.LatLng(lat, lng);
      const marker = new window.kakao.maps.Marker({
        position: latlng,
        map: this.map,
      });

      // Make sure the stores array is initialized
      if (!this.stores[index]) {
        this.stores[index] = {};
      }

      // Attach the marker to the store object
      this.stores[index].marker = marker;

      // Add event listener for displaying place name on marker click
      window.kakao.maps.event.addListener(marker, 'click', () => {
        this.showPlaceName(name, latlng);
      });
    },
    calculateDistance() {
      const addressLatLng = new window.kakao.maps.LatLng(this.address.lat, this.address.lng);

      this.stores.forEach((store, index) => {
        const latlng2 = store.marker.getPosition();
        this.drawConnectingLine(addressLatLng, latlng2, index);
      });
    },
    drawConnectingLine(latlng1, latlng2, index) {
      const line = new window.kakao.maps.Polyline({
        path: [latlng1, latlng2],
        strokeWeight: 3,
        strokeColor: "#FF0000",
        strokeOpacity: 0.7,
      });
      line.setMap(this.map);

      const distance = this.calculateDistanceBetween(latlng1, latlng2);

      // Create a content for CustomOverlay
      const content = `<div style="padding:5px;">Distance: ${distance.toFixed(2)} m</div>`;

      // Attach the content to CustomOverlay
      const customOverlay = new window.kakao.maps.CustomOverlay({
        content,
        position: latlng2,
        xAnchor: 0.5,
        yAnchor: -1.5,
      });

      customOverlay.setMap(this.map);

      // Attach the custom overlay to the store object
      this.stores[index].overlay = customOverlay;
    },
    calculateDistanceBetween(latlng1, latlng2) {
      const rad = Math.PI / 180;
      const lat1 = latlng1.getLat() * rad;
      const lng1 = latlng1.getLng() * rad;
      const lat2 = latlng2.getLat() * rad;
      const lng2 = latlng2.getLng() * rad;
      const dlat = lat2 - lat1;
      const dlng = lng2 - lng1;
      const a =
        Math.sin(dlat / 2) ** 2 +
        Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlng / 2) ** 2;
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      const radius = 6371 * 1000; // Earth's radius in meters
      return radius * c;
    },
    showPlaceName(name, latlng) {
      const content = `<div style="padding:5px;">${name}</div>`;

      // Create an overlay for displaying place name
      const overlay = new window.kakao.maps.CustomOverlay({
        content,
        position: latlng,
        xAnchor: 0.5,
        yAnchor: 1.5,
      });

      overlay.setMap(this.map);

      // Automatically close the overlay after 3 seconds
      setTimeout(() => {
        overlay.setMap(null);
      }, 3000);
    },
  },
};

</script>

<style scoped>
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

