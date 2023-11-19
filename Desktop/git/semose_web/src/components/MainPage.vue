<template>
  <div class="mastscreen">
    <div class="container">
      <div class="left-column">
        <!-- 좌측 컬럼의 내용 -->

          <div>
        <!-- 주소 입력 컴포넌트를 상위 컴포넌트에서 사용 -->
          <div>
            입력된 주소 : {{post_data.address}}
          </div>
            <form-component 
            @onUpdateAddress="onUpdateAddress"
            @onUpdateStore="onUpdateStore"
            >
            </form-component>
          <div>

          <div>
            data : {{data}}
          </div>
          <kakao-map :parentData="data">
          </kakao-map>
          </div>
      </div>
      <div class="right-column">
        <!-- 우측 컬럼의 내용 -->
      </div>
    </div>
  </div>
  </div>
</template>


<script>

import axios from "axios";
import FormComponent from './FormComponent.vue';
import MapComponent from './MapComponent.vue';


export default {
  components : {
    'form-component': FormComponent,
    'kakao-map': MapComponent,
  },
  data() {
    return {
      data: {
        scorebox : null,
        info_store : [
          { name: "스타벅스", lat: 37.2796352, lng: 127.043346 },
          { name: "Burger King", lat: 37.2745815, lng: 127.045215 },
          { name: "Daiso", lat: 37.2754895, lng: 127.0423236 },
        ]
      },
      address: '',
      selected: [],
      post_data:{
        "address" : "",
        "selected" : [],
      }
    };
  },
  methods: {
    onGetData() {
    axios
      .get(`http://localhost:8000/api/end`, {})
      .then((res) => {
        console.log("---axios Get 성공---- ");
        const receivedData = res.data;

        // 받은 데이터를 Vue 데이터 형식에 맞게 가공
        const processedData = {
          scorebox: receivedData.scorebox,
          info_store: JSON.parse(receivedData.info_store)
        };

        // Vue 데이터에 할당
        this.data = processedData;
      })
      .catch((res) => {
        console.error(res);
      });
  },
    onUpdateAddress(newAddress) {
      // 하위 컴포넌트에서 전달된 새로운 주소 값을 상위 컴포넌트의 데이터에 적용
      this.post_data.address = newAddress;
    },
    onUpdateStore(newStore) {
      // 하위 컴포넌트에서 전달된 새로운 주소 값을 상위 컴포넌트의 데이터에 적용
      this.post_data.selected = newStore;
      this.fullRequest()
    },
    sendDataToServer() {
      axios
        .post(`http://localhost:8000/api/end`, {
          address: this.post_data.address,
          selected: JSON.stringify(this.post_data.selected),
        })
        .then((res) => {
          console.log("---axios Post 성공---- ");
          console.log(res.data)
        })
        .catch((res) => {
          console.error(res);
        });
      this.sendLogToServer();
    },
    sendLogToServer() {
      axios
      .post('http://localhost:8000/api/log', {
        address: this.post_data.address,
        selected: JSON.stringify(this.post_data.selected),
      })
      .then((res) => {
        console.log('Data posted successfully');
        this.data = res.data;
      })
      .catch((res) => {
        console.error('Error posting data:', res);
      });
    },
    fullRequest(){
      this.sendDataToServer()
      this.onGetData()
      this.sendLogToServer()
    }
  },
};
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');


.mastscreen {
  background-image: url("../assets/resources/assets/img/header-bg.jpg");
  background-repeat: no-repeat;
  background-attachment: scroll;
  background-position: center center;
  background-size: cover;
}

.container {
  display: flex; /* Flexbox 사용 */
  justify-content: space-between; /* 좌우로 공간 분배 */
}

.left-column {
  flex: 1; /* 좌측 컬럼이 나머지 공간을 채우도록 설정 */
}

.right-column {
  flex: 1; /* 우측 컬럼이 나머지 공간을 채우도록 설정 */
}

/* 필요에 따라 컬럼 스타일을 조정할 수 있습니다. */
</style>






