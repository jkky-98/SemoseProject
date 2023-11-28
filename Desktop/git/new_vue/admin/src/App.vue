<template>
  <router-view></router-view>
</template>

<script>
import "@/styles/overrides.sass";

export default {
  name: "App",
};
</script>
<style>
.v-application {
  font-family: "NanumBarunGothic", sans-serif !important;
}
@font-face {
  font-family: "NanumBarunGothic";
  src: url("./assets/NanumBarunGothic.ttf") format("truetype");
  font-weight: 400;
}
</style>
