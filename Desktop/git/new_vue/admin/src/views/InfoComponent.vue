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
                <!-- 데이터가 있을 때 -->
                <v-card
                  v-if="
                    data_info && data_info.scorebox && data_info.scorebox.score
                  "
                >
                  <v-card
                    class="pa-3"
                    outlined
                    width="100%"
                    height="100%"
                    color="#26293C"
                    dark
                  >
                    <v-card-title
                      class="justify-center text-h5 font-weight-bold"
                      >Present Address</v-card-title
                    >
                    <v-card-title class="title">
                      {{ myOnerooms[0].title }}
                    </v-card-title>
                    <v-card-subtitle class="subtitle">
                      아주대로 부터 {{ myOnerooms[0].distance.toFixed(1) }} 분
                      거리에 있습니다.
                    </v-card-subtitle>
                    <v-card-text>
                      <div>면적(평): {{ myOnerooms[0].area_p }}평</div>
                      <div>층: {{ myOnerooms[0].floor }}층</div>
                      <div>
                        보증금(전,월세): {{ myOnerooms[0].deposit }}만원
                      </div>
                      <div>관리비 : {{ myOnerooms[0].manage_cost }}만원</div>
                      <div>월세: {{ myOnerooms[0].rent }}만원</div>
                      <div>전/월세: {{ myOnerooms[0].sales_type }}</div>
                      <div>
                        등록시간:
                        {{ formatToLocalTime(myOnerooms[0].reg_date) }}
                      </div>
                      <v-btn
                        block
                        :href="
                          'https://www.zigbang.com/home/oneroom/items/' +
                          myOnerooms[0].item_id
                        "
                        target="_blank"
                        color="#F87979"
                        >직방에서 보기</v-btn
                      >
                    </v-card-text>
                  </v-card>
                  <!-- 여기에 데이터 표시하는 다른 요소들 추가 가능 -->
                </v-card>

                <!-- 데이터가 없을 때 -->
                <v-card v-else>
                  <v-card-text class="text-center text-h5 font-weight-bold">
                    조건설정을 완료해주세요.
                  </v-card-text>
                  <!-- 맵 로딩을 위한 요소들 추가 가능 -->
                </v-card>
                <!-- 여기에 데이터 표시하는 다른 요소들 추가 가능 -->
              </v-card>

              <!-- 데이터가 없을 때 -->
              <v-card v-else>
                <v-card-text class="text-center text-h5 font-weight-bold">
                  조건설정을 완료해주세요.
                </v-card-text>
                <!-- 맵 로딩을 위한 요소들 추가 가능 -->
              </v-card>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="pa-0" outlined>
              <!-- <v-img src="@/assets/cluster_img.jpg"></v-img> -->
              <v-card
                class="pa-3"
                outlined
                elevation="10"
                width="100%"
                color="#26293C"
                dark
              >
                <bar-chart />
              </v-card>
            </v-card>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-col col="6">
          <v-card class="pa-3" outlined width="100%" color="#26293C" dark>
            <v-card-title class="justify-center text-h5 font-weight-bold"
              >Recommend List</v-card-title
            >
            <v-data-table
              :headers="headers"
              :items="filteredData"
              :items-per-page="5"
              class="elevation-1"
              multi-sort
              :sort-desc="[false, true]"
              loading
              loading-text="Loading... Please wait"
              :single-expand="singleExpand"
              :expanded.sync="expanded"
              show-expand
              item-key="item_id"
            >
              <template v-slot:top>
                <v-toolbar flat>
                  <v-toolbar-title
                    >현재 클러스터 :
                    {{ myOnerooms[0].cluster }}</v-toolbar-title
                  >
                  <v-spacer></v-spacer>
                  <v-switch
                    v-model="singleExpand"
                    label="Single expand"
                    class="mt-2"
                  ></v-switch>
                </v-toolbar>
              </template>
              <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length">
                  <v-btn
                    block
                    :href="
                      'https://www.zigbang.com/home/oneroom/items/' +
                      item.item_id
                    "
                    target="_blank"
                    >직방에서 보기</v-btn
                  >
                  <v-btn
                    block
                    @click="settingaddress(item.lat, item.lng, item.title)"
                    >이 매물 주소에 적용
                  </v-btn>
                </td>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card
            class="pa-3"
            outlined
            elevation="10"
            width="100%"
            color="#26293C"
            dark
          >
            <bubble-chart />
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card
            class="pa-3"
            outlined
            elevation="10"
            width="100%"
            color="#26293C"
            dark
          >
            <v-img src="@/assets/cluster_img.jpg"></v-img>
          </v-card>
        </v-col>
      </v-card>
    </v-container>
    <v-snackbar v-model="snackbar" :multi-line="multiLine">
      조건설정이 필요합니다.

      <template v-slot:action="{ attrs }">
        <v-btn color="red" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";
import BarChart from "@/components/BarChart.vue";
import BubbleChart from "@/components/BubbleChart.vue";
import axios from "axios";

export default {
  data: () => ({
    multiLine: true,
    snackbar: false,
    cluster_percost_list: [],
    expanded: [],
    singleExpand: false,
    headers: [
      {
        text: "직방 매물",
        align: "start",
        sortable: false,
        value: "title",
      },
      { text: "거리(분-보행)", value: "distance" },
      { text: "월세(만원)", value: "rent" },
      { text: "보증금(만원)", value: "deposit" },
      { text: "평수(평)", value: "area_p" },
      { text: "관리비(만원)", value: "manage_cost" },
      { text: "층수(층)", value: "floor" },
      { text: "", value: "data-table-expand" },
    ],
    choose_zickbang: [{ lat: null, lng: null }],
    thenData: null,
    myData: [
      {
        title: "아주대 인근 원룸",
        distance: 10,
        area_p: 10,
        floor: 3,
        deposit: 1000,
        rent: 100,
        manage_cost: 5,
        sales_type: "월세",
        reg_date: "2021-05-01T00:00:00.000Z",
        item_id: 1083533,
        my: true,
      },
    ],
  }),
  watch: {
    // data_info.scorebox.score의 변경을 감지
    "data_info.scorebox.score": {
      handler(newVal) {
        // 데이터가 없으면 snackbar를 보여줌
        this.snackbar = !newVal;
      },
      immediate: true, // 초기화 시 즉시 실행
    },
  },
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
  components: {
    "bar-chart": BarChart,
    "bubble-chart": BubbleChart,
  },
  computed: {
    ...mapState({
      myAddress: "address",
      buttons: "buttons",
      zickbang_point: "zickbang_point",
      data: "receivedData",
      data_info: "receivedData_info",
    }),
    myOnerooms() {
      return this.$store.getters.getMyOnerooms(true);
    },
    filteredData() {
      const others = this.$store.getters.getMyOnerooms(false);
      if (!others || !others.length) {
        return [];
      }

      const my_d = this.$store.getters.getMyOnerooms(true);

      if (!my_d.length) {
        return others;
      }

      const myCluster = my_d[0].cluster;
      // others 배열에서 cluster 값이 myCluster와 일치하는 항목만 반환
      return others.filter((item) => item.cluster === myCluster);
    },
  },
  methods: {
    formatToLocalTime(dateTimeString) {
      const dateObj = new Date(dateTimeString);
      return dateObj.toLocaleString(); // 현재 브라우저의 로컬 시간으로 변환하여 반환
    },
    settingaddress(lat, lng, title) {
      // Vuex store에 값을 저장합니다.
      this.$nextTick(() => {
        this.$set(this.choose_zickbang, 0, { lat, lng, title });
      });
      this.$nextTick(() => {
        this.$store.commit("SET_ZICKBANG_POINT", this.choose_zickbang);
      });
      this.$store.dispatch("clearAddress");
      this.$nextTick(() => {
        this.reMountPost();
      });
    },
    async reMountPost() {
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
        this.$nextTick(() => {
          this.$store.dispatch("clearRecievedData");
        });
        this.$nextTick(() => {
          this.$store.commit("SET_RECEIVED_DATA_INFO", processedData);
        });
        console.log("postthen vuex 저장 완료");
      } catch (error) {
        console.error(error.message);
        // 에러 메시지 처리 등
      }
    },
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
