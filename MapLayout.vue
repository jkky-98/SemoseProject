<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div id="map" ref="map"></div>
  </div>
</template>

<script>
export default {
  name: 'MapLayout',
  data() {
    return {
      msg: '세모세에 오신 것을 환영합니다!'
    };
  },
  mounted() {
    // Initialize Kakao Map once the component is mounted
    const mapContainer = this.$refs.map;
    const mapOption = {
      center: new window.kakao.maps.LatLng(33.450701, 126.570667),
      level: 3
    };

    // Create a map with the div to display the map and map options
    const map = new window.kakao.maps.Map(mapContainer, mapOption);

    // Use the map variable here
    const marker = new window.kakao.maps.Marker({
      position: new window.kakao.maps.LatLng(33.450701, 126.570667),
      map: map
    });

    // If you want to interact with the marker or perform other actions, use it here
    // For example, you can add an event listener to the marker:
    window.kakao.maps.event.addListener(marker, 'click', function() {
      // Handle marker click event
      console.log('Marker clicked');
    });
  }
};
</script>

<style scoped lang="scss">
h1 {
  margin: 40px 0 0;
}

#map {
  width: 100%;
  height: 400px; /* Set the desired height for your map */
  border: 1px solid #000; /* Add a border to see the map container */
}
</style>
