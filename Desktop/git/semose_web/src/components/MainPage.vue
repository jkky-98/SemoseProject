<template>
  <div class="mastscreen">
    <div class="container">
      <div class="left-column">
        <!-- 좌측 컬럼의 내용 -->

          <div>
        <!-- 주소 입력 컴포넌트를 상위 컴포넌트에서 사용 -->
            <address-component @onUpdateAddress="onUpdateAddress">
            </address-component>

            <address-search @onUpdateAddress="onUpdateAddress">
            </address-search>
          <div>
            입력된 주소 : {{post_data.address}}
          </div>
            <form-component 
            @onUpdateAddress="onUpdateAddress"
            @onUpdateStore="onUpdateStore"
            >
            </form-component>
          <div>
            <b-col class="pb-2" >
              <b-button size="lg" 
              style="font-size: 30px; font-weight: bold; margin: 20px 0;"
              variant="info"
              @click="sendDataToServer"
              >START
              </b-button>
            </b-col>

            <b-col class="pb-2" >
              <b-button size="lg" 
              style="font-size: 30px; font-weight: bold; margin: 20px 0;"
              variant="info"
              @click="onClickGetData"
              >START
              </b-button>
            </b-col>
          <div>
            data : {{data}}
          </div>

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
import Address from './Address.vue';
import AddressSearch from './AddressSearch.vue';
import FormComponent from './FormComponent.vue';



export default {
  components : {
    'address-component': Address,
    'address-search': AddressSearch,
    'form-component': FormComponent,
  },
  data() {
    return {
      data: null,
      address: '',
      selected: [],
      post_data:{
        "address" : "",
        "selected" : [],
      }
    };
  },
  methods: {
    onClickGetData() {
      axios
        .get(`http://localhost:8000/api/end`, {})
        .then((res) => {
          console.log("---axios Get 성공---- ");
          this.data = res.data;
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
    },
    sendDataToServer() {
      axios
        .post(`http://localhost:8000/api/end`, {
          address: this.post_data.address,
          selected: JSON.stringify(this.post_data.selected),
        })
        .then((res) => {
          console.log("---axios Post 성공---- ");
          this.data = res.data;
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






