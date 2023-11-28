<template>
  <div>
    <v-container fluid>
      <v-card class="pa-3">
        <v-row>
          <v-col cols="3">
            <v-card class="pa-3" outlined elevation="10">
              <v-card-title>SCORE</v-card-title>
              <span class="score">{{ this.data.scorebox.score }}</span>
            </v-card>
          </v-col>
          <v-col cols="3">
            <v-card class="pa-3" outlined> </v-card>
          </v-col>
          <v-col cols="6">
            <v-card class="pa-0" outlined>
              <v-img src="@/assets/cluster_img.jpg"></v-img>
            </v-card>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState({
      myAddress: "address",
      buttons: "buttons",
      zickbang_point: "zickbang_point",
      data: "receivedData",
    }),
  },
};
</script>

<style>
.score {
  font-size: 24px;
  font-weight: bold;
}

/* 추가적인 스타일링을 위한 클래스 또는 선택자를 여기에 추가하세요 */
</style>
