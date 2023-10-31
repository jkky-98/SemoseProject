<template>
  <div class="intro">
    <div class="intro-inner">
      <!-- 이미지 추가 -->
      <img alt="Vue logo" :src="require('@/assets/saemose.png')">
      <h1>세상의<br>모든 세권</h1>
      <router-link 
        class="button" 
        :to="todayUrl"
      > START 
      </router-link>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'IntroSection',
  methods: {},
  computed: {
    todayUrl() {
      let todayUrl = moment(new Date()).format('YYYY-MM-DD');
      return `/day/${todayUrl}`;
    },
  },
  props: {},
};
</script>

  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
  