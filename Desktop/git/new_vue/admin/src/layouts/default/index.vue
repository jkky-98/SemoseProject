<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>
        {{ $route.meta.dynamicTitle }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      app
      src="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h3 white--text">
            SEMOSE
          </v-list-item-title>
          <v-list-item-subtitle class="white--text">
            Capstone Project
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          link
          :to="item.to"
        >
          <v-list-item-icon>
            <v-icon class="white--text">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="white--text">{{
              item.title
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn :color="isDataAvailable ? 'success' : 'error'" block>
            {{ isDataAvailable ? "조건 선택 완료" : "조건 선택 필요" }}
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "DefaultLayout",
  data: () => ({
    drawer: false,
    gradient: "rgba(0, 0, 0, .7), rgba(0, 0, 0, .7)",
    items: [
      {
        title: "세권 조건 선택",
        icon: "mdi-account-multiple-plus",
        to: "/",
        dynamicTitle: "세권 조건 선택",
      },
      {
        title: "세권 지도",
        icon: "mdi-map-marker-distance",
        to: "/map",
        dynamicTitle: "세권 지도",
      },
      {
        title: "세권 상세정보",
        icon: "mdi-view-dashboard",
        to: "/info",
        dynamicTitle: "세권 상세정보",
      },
    ],
  }),
  computed: {
    isDataAvailable() {
      // Vuex에서 address와 zickbang_point 데이터가 있는지 확인하는 computed 속성
      const { address, zickbang_point } = this.$store.state;
      return !!address || (zickbang_point && zickbang_point.length > 0);
    },
  },
};
</script>

<style></style>
