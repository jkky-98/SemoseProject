<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="3">
          <!-- 왼쪽 영역에 주소 정보를 감싸는 박스 -->
          <v-card class="pa-3">
            <v-row>
              <v-col>
                <!-- 주소 정보 -->
                <v-card>
                  <v-card-title class="text-h6">
                    <span v-if="address">{{ address }}</span>
                    <span v-else-if="zickbang_point.length">{{
                      zickbang_point
                    }}</span>
                    <span v-else>Enter your address</span>

                    <div>
                      <span
                        v-if="address || zickbang_point.length"
                        class="sub-title-message"
                      >
                        {{
                          address
                            ? "주소가 입력되었습니다."
                            : "zickbang_point가 입력되었습니다."
                        }}
                      </span>
                    </div>
                  </v-card-title>
                  <v-card-text :value="address">
                    <v-btn
                      block
                      :color="buttonClicked ? 'success' : ''"
                      @click="execDaumPostcode"
                      >주소검색</v-btn
                    >
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <!-- 추가 행 -->
            <v-row>
              <v-col>
                <v-card color="#272727">
                  <v-card-title class="text-center justify-center py-6">
                    <h1 class="font-weight-bold text-h2">Store</h1>
                  </v-card-title>

                  <v-tabs v-model="tab" background-color="transparent" grow>
                    <v-tab v-for="item in items" :key="item.id">
                      {{ item }}
                    </v-tab>
                  </v-tabs>

                  <v-tabs-items v-model="tab">
                    <v-tab-item v-for="item in storeList" :key="item.id">
                      <v-card color="#272727" flat>
                        <v-card-text>
                          <v-btn
                            v-for="(btn, index) in item"
                            :key="index"
                            :color="isSelected(btn) ? 'info' : ''"
                            @click="handleButtonClick(btn)"
                          >
                            {{ btn }}
                          </v-btn>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>
                  </v-tabs-items>
                </v-card>
              </v-col>
            </v-row>
            <!-- 추가 행 -->
            <v-row>
              <v-col>
                <v-card color="#272727">
                  <v-card-title
                    class="text-center justify-center font-weight-bold text-h4"
                    >선택한 Store</v-card-title
                  >
                  <v-card-text>
                    <div>
                      <v-btn v-for="(button, index) in buttons" :key="index">
                        {{ button }}
                      </v-btn>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <!-- 추가 행 -->
          </v-card>
          <v-carousel v-model="model">
            <v-carousel-item v-for="(color, i) in explain.colors" :key="color">
              <v-sheet :color="color" height="100%" tile>
                <v-row class="fill-height" align="center" justify="center">
                  <div class="text-h5">{{ explain.ex[i] }}</div>
                </v-row>
              </v-sheet>
            </v-carousel-item>
          </v-carousel>
          <v-footer dark padless>
            <v-card flat tile class="indigo lighten-1 white--text text-center">
              <v-card-text>
                <v-btn
                  v-for="icon in icons"
                  :key="icon"
                  class="mx-4 white--text"
                  icon
                >
                  <v-icon size="24px">
                    {{ icon }}
                  </v-icon>
                </v-btn>
              </v-card-text>

              <v-card-text class="white--text pt-0">
                If you want contact us, please click. Thank you for using our
                Service
              </v-card-text>

              <v-divider></v-divider>

              <v-card-text class="white--text">
                {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
              </v-card-text>
            </v-card>
          </v-footer>
        </v-col>
        <v-col cols="9">
          <!-- 오른쪽 영역 -->
          <v-card class="pa-3" v-if="success_zicbang">
            <v-row>
              <v-col
                v-for="(item, index) in visibleItems"
                :key="index"
                cols="12"
                md="6"
                lg="4"
              >
                <v-card>
                  <v-img
                    height="250"
                    :src="item.images_thumbnail + '?h=300'"
                  ></v-img>

                  <v-card-title class="title">
                    {{ item.title }}
                  </v-card-title>
                  <v-card-subtitle class="subtitle">
                    아주대로 부터 {{ item.distance.toFixed(1) }} 분 거리에
                    있습니다.
                  </v-card-subtitle>
                  <v-card-text>
                    <div>면적(평): {{ item.area_p }}평</div>
                    <div>층: {{ item.floor }}층</div>
                    <div>보증금(전,월세): {{ item.deposit }}만원</div>
                    <div>관리비 : {{ item.manage_cost }}만원</div>
                    <div>월세: {{ item.rent }}</div>
                    <div>전/월세: {{ item.sales_type }}</div>
                    <div>등록시간: {{ formatToLocalTime(item.reg_date) }}</div>
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
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-pagination
              v-model="currentPage"
              :length="totalPages"
            ></v-pagination>
          </v-card>
        </v-col>
        <v-col col="12">
          <v-card class="pa-3" color="#272727">
            <v-row>
              <v-col>
                <v-card class="pa-3" outlined>
                  <kakao-map-dash ref="kakaoMap" />
                </v-card>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
import KakaoMap_dash from "@/components/KakaoMap_dash.vue";

export default {
  components: {
    "kakao-map-dash": KakaoMap_dash,
  },
  computed: {
    ...mapState({
      address: (state) => state.address,
      buttons: (state) => state.buttons,
      zickbang_point: (state) => state.zickbang_point,
      dash_zickbang_source: (state) => state.dash_zickbang_source,
    }),
    visibleItems() {
      if (!this.success_zicbang) return []; // 데이터가 없는 경우 빈 배열 반환
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;

      return this.zicbang_source.slice(startIndex, endIndex);
    },
    totalPages() {
      if (!this.zicbang_source) return 0; // 데이터가 없는 경우 0 반환

      return Math.ceil(this.zicbang_source.length / this.itemsPerPage);
    },
  },
  async mounted() {
    try {
      if (this.buttons.length === 0) {
        this.$store.commit("SET_DEFAULT_BUTTONS", this.selectedButtons);
      }

      const response = await axios.get("http://localhost:8000/api/zicbang");
      const dataArray = JSON.parse(response.data.data);

      this.zicbang_source = dataArray;
      this.success_zicbang = true;
      this.$nextTick(() => {
        this.$store.dispatch("setDash_zickbang_source", this.zicbang_source);
      });
      this.$nextTick(() => {
        this.$refs.kakaoMap.reLoadMap(this.dash_zickbang_source);
      });
      console.log("axios success");
    } catch (error) {
      console.error("Error fetching data", error);
    }
  },

  data() {
    return {
      model: 0,
      explain: {
        colors: ["secondary", "primary", "yellow darken-2"],
        ex: [
          "첫번째 탭에서 세권 조건을 선택해주세요",
          "Map Rendering을 진행해주세요.",
          "상세정보 페이지를 볼 수 있어요.",
        ],
      },
      currentPage: 1,
      itemsPerPage: 6,
      zicbang_source: [],
      success_zicbang: false,
      choose_zickbang: [{ lat: null, lng: null }],
      icons: ["mdi-facebook", "mdi-twitter", "mdi-linkedin", "mdi-instagram"],
      buttonClicked: false,
      selectedButtons: [
        "편의점",
        "카페",
        "약국",
        "세탁소",
        "대형마켓",
        "아주대학교",
      ],
      tab: null,
      items: ["중요", "편의시설", "문화시설", "프랜차이즈", "카페"],
      storeList: {
        중요: ["편의점", "카페", "약국", "세탁소", "대형마켓", "아주대학교"],
        편의시설: ["인쇄", "PC방", "내과", "한의원", "우체국", "올리브영"],
        문화시설: ["영화관", "헬스장", "필라테스", "코인노래방", "공원"],
        프랜차이즈: [
          "맥도날드",
          "롯데리아",
          "버거킹",
          "베스킨라빈스",
          "파리바게뜨",
        ],
        카페: [
          "스타벅스",
          "메가커피",
          "컴포즈커피",
          "빽다방",
          "이디야커피",
          "투썸플레이스",
        ],
      },
      // daum post code data //
      postcode: "",
      dataAddress: "",
      extraAddress: "",
      // daum post code data //
    };
  },
  methods: {
    settingaddress(lat, lng, title) {
      // Vuex store에 값을 저장합니다.
      this.$set(this.choose_zickbang, 0, { lat, lng, title });
      this.$store.commit("SET_ZICKBANG_POINT", this.choose_zickbang);
      this.$store.dispatch("clearAddress");
      this.$forceUpdate();
    },
    formatToLocalTime(dateTimeString) {
      const dateObj = new Date(dateTimeString);
      return dateObj.toLocaleString(); // 현재 브라우저의 로컬 시간으로 변환하여 반환
    },
    executeFunction() {
      // 실행하고자 하는 기능을 여기에 작성
      console.log("주소 검색 버튼이 클릭되었습니다.");
      // 버튼 클릭 시 색 변경
      this.buttonClicked = !this.buttonClicked;
      // 기능 실행 로직을 추가하세요
    },
    handleButtonClick(storeName) {
      const index = this.buttons.indexOf(storeName);
      if (index !== -1) {
        // 이미 선택된 버튼인 경우 배열에서 제거하여 비활성화
        this.buttons.splice(index, 1);
      } else {
        // 선택되지 않은 경우 배열에 추가하여 활성화
        this.buttons.push(storeName);
      }
    },
    isSelected(storeName) {
      return this.buttons.includes(storeName);
    },
    // Daum 주소 검색기
    execDaumPostcode() {
      new window.daum.Postcode({
        oncomplete: (data) => {
          if (this.extraAddress !== "") {
            this.extraAddress = "";
          }
          if (data.userSelectedType === "R") {
            // 사용자가 도로명 주소를 선택했을 경우
            this.dataAddress = data.roadAddress;
          } else {
            // 사용자가 지번 주소를 선택했을 경우(J)
            this.dataAddress = data.jibunAddress;
          }

          // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
          if (data.userSelectedType === "R") {
            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if (data.bname !== "" && /[동|로|가]$/g.test(data.bname)) {
              this.extraAddress += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if (data.buildingName !== "" && data.apartment === "Y") {
              this.extraAddress +=
                this.extraAddress !== ""
                  ? `, ${data.buildingName}`
                  : data.buildingName;
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if (this.extraAddress !== "") {
              this.extraAddress = `(${this.extraAddress})`;
            }
          } else {
            this.extraAddress = "";
          }
          // 우편번호를 입력한다.
          this.postcode = data.zonecode;
          // Vuex 액션 호출하여 주소 저장
          this.$store.dispatch("saveAddress", this.dataAddress);
          this.$store.dispatch("clearZickbangPoint");
        },
      }).open();
    },
  },
};
</script>
<style scoped>
/* Helper classes */
.basil {
  background-color: white !important;
}
.basil--text {
  color: #010302 !important;
}
.sub-title-message {
  font-size: 0.8em; /* 작은 글씨 */
  color: #67c23a; /* 밝은 초록색 */
  display: block; /* 한 줄로 표시되도록 변경 */
  margin-top: 4px; /* 위쪽 여백 추가 */
}
</style>
