<template>
  <div>
    <v-container fluid>
      <v-card class="pa-3" color="#272727">
        <v-row>
          <v-col>
            <v-card class="pa-3" outlined>
              <v-btn color="primary" block @click="postData"
                >Map Rendering</v-btn
              >
              <v-card-text class="text-center text-h5 font-weight-bold"
                >MAP VIEW
              </v-card-text>
              <kakao-map ref="kakaoMap" />
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import KakaoMap from "@/components/KakaoMap.vue";
import { mapState } from "vuex";
import axios from "axios";

export default {
  data: () => ({
    thenData: null,
  }),
  computed: {
    ...mapState({
      myAddress: "address",
      buttons: "buttons",
      zickbang_point: "zickbang_point",
      data: "receivedData",
    }),
  },
  components: {
    "kakao-map": KakaoMap,
  },
  methods: {
    async postData() {
      try {
        let dataToSend = null;
        const startTime = performance.now();
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

        const res = await axios.post(`http://localhost:8000/api/end`, {
          address: dataToSend,
          selected: JSON.stringify(this.buttons),
        });

        console.log("---axios Post 성공---- ");
        const receivedData = res.data;

        const processedData = {
          scorebox: receivedData.scorebox,
          info_store: JSON.parse(receivedData.info_store),
          address_latlng: receivedData.address_point,
          bus: JSON.parse(receivedData.bus_data),
        };

        // Vue 데이터에 할당
        this.thendata = processedData;

        // Vuex 스토어에 데이터 저장
        this.$store.commit("SET_RECEIVED_DATA", processedData);
        console.log("postthen vuex 저장 완료");
        this.$refs.kakaoMap.reLoadMap();
        const endTime = performance.now(); // 요청 완료 시간 기록
        const duration = endTime - startTime; // 요청 처리 시간 계산 (밀리초 단위)
        console.log(`Axios 요청 처리 시간: ${duration}ms`);
      } catch (error) {
        console.error(error.message);
        // 에러 메시지 처리 등
      }
    },
  },
};
</script>
