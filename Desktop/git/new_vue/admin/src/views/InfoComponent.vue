<template>
  <div class="page-background">
    <v-container fluid>
      <v-card class="pa-3">
        <v-row>
          <v-col cols="6">
            <v-card
              class="pa-3"
              outlined
              elevation="10"
              width="100%"
              color="#26293C"
              dark
            >
              <v-card-title class="justify-center text-h5 font-weight-bold"
                >SCORE</v-card-title
              >
              <!-- 데이터가 있을 때 -->
              <v-card
                v-if="
                  data_info && data_info.scorebox && data_info.scorebox.score
                "
              >
                <v-card-text class="text-center text-h1 font-weight-bold">
                  {{ data_info.scorebox.score }}
                </v-card-text>
                <!-- 여기에 데이터 표시하는 다른 요소들 추가 가능 -->
              </v-card>

              <!-- 데이터가 없을 때 -->
              <v-card v-else>
                <v-card-text class="text-center text-h5 font-weight-bold">
                  맵 로딩을 해주세요.
                </v-card-text>
                <!-- 맵 로딩을 위한 요소들 추가 가능 -->
              </v-card>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card
              class="pa-3"
              outlined
              elevation="10"
              width="100%"
              color="#26293C"
              dark
            >
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="pa-0" outlined>
              <!-- <v-img src="@/assets/cluster_img.jpg"></v-img> -->
              <BarChart />
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import BarChart from "@/components/BarChart.vue";
import axios from "axios";

export default {
  data: () => ({
    thenData: null,
  }),
  async mounted() {
    try {
      let dataToSend = null;
      console.log(this.myAddress);
      console.log(this.zickbang_point);

      if (
        !this.myAddress &&
        Array.isArray(this.zickbang_point) &&
        this.zickbang_point.length > 0
      ) {
        dataToSend = this.zickbang_point;
      } else if (
        this.myAddress &&
        (!this.zickbang_point ||
          (Array.isArray(this.zickbang_point) &&
            this.zickbang_point.length === 0))
      ) {
        dataToSend = this.myAddress;
      } else {
        throw new Error("주소 또는 zickbang_point가 필요합니다.");
      }

      const res = await axios.post(`http://localhost:8000/api/info`, {
        address: dataToSend,
        selected: JSON.stringify(this.buttons),
      });

      console.log("---axios Post 성공---- /info ");
      const receivedData = res.data;

      const processedData = {
        scorebox: receivedData.scorebox,
        info_store: JSON.parse(receivedData.info_store),
        address_latlng: receivedData.address_point,
        bus: JSON.parse(receivedData.bus_data),
        oneroom_all: JSON.parse(receivedData.oneroom_data_cluster),
        oneroom_data_cluster: receivedData.my_data,
      };

      // Vue 데이터에 할당
      this.thendata = processedData;

      // Vuex 스토어에 데이터 저장
      this.$store.commit("SET_RECEIVED_DATA_INFO", processedData);
      console.log("postthen vuex 저장 완료");
    } catch (error) {
      console.error(error.message);
      // 에러 메시지 처리 등
    }
  },
  components: { BarChart },
  computed: {
    ...mapState({
      myAddress: "address",
      buttons: "buttons",
      zickbang_point: "zickbang_point",
      data: "receivedData",
      data_info: "receivedData_info",
    }),
  },
};
</script>

<style>
.score {
  font-size: 50px;
  font-weight: bold;
  text-align: center;
  /* 만약 화면 전체를 가운데 정렬하고 싶다면 아래와 같이 사용합니다 */
  /* display: flex;
  justify-content: center;
  align-items: center; */
}
.card-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}
.page-background {
  background-color: #1e1e2f; /* 적용할 배경색 코드를 입력하세요 */
  width: 100%;
  height: 100%;
  /* 기타 스타일링을 원하면 여기에 추가하세요 */
}
/* 추가적인 스타일링을 위한 클래스 또는 선택자를 여기에 추가하세요 */
</style>
