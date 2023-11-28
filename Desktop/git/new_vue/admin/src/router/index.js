import Vue from "vue";
import VueRouter from "vue-router";
import DashBoard from "../views/DashBoard.vue";
import MapComponent from "../views/MapComponent.vue";
import DefaultLayout from "../layouts/default/index.vue";
import InfoComponent from "../views/InfoComponent.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      {
        path: "/",
        name: "DashBoard",
        component: DashBoard,
        meta: {
          title: "세권 조건 선택",
          dynamicTitle: "세권 조건 선택",
        },
      },
      {
        path: "/map",
        name: "MapComponent",
        component: MapComponent,
        meta: {
          title: "세권 지도",
          dynamicTitle: "세권 지도",
        },
      },
      {
        path: "/info",
        name: "InfoComponent",
        component: InfoComponent,
        meta: {
          title: "세권 상세정보",
          dynamicTitle: "세권 상세정보",
        },
      },
    ],
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
