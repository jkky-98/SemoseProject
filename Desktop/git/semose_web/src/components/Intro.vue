<template>
  <header class='masthead'>
    
      <div class='masthead-subheading'>Welcome To Our Service!</div>
      <div class='masthead-heading text-uppercase'>SEMOSE</div>
      <b-col class="pb-2" >
        <b-button size="lg" 
        style="font-size: 40px; font-weight: bold;"
        variant="info"
        to = "/main"
        >START
        </b-button>
      </b-col>

  </header>
</template>

<script>

export default {
  name: 'IntroComponent',
  components: {
  },
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');
@import '../assets/resources/css/styles.css';

.start-screen {
  background-image: url('../assets/Sexy Blue.jpg');
  background-size: cover;
  background-position: center;
}
.header-font {
  font-family: 'Lilita One', cursive;
  color: white;
  position: relative;
}
.top-right-text {
  position: absolute; /* 상대 위치 요소에 대해 절대 위치로 설정 */
  top: 0px; /* 위에서 0px 떨어진 위치 (오른쪽 상단) */
  left: 40px; /* 오른쪽에서 0px 떨어진 위치 (오른쪽 상단) */
  font-size: 70px;
}
.masthead {
  padding-top: 10.5rem;
  padding-bottom: 6rem;
  text-align: center;
  color: #fff;
  background-image: url("../assets/resources/assets/img/header-bg.jpg");
  background-repeat: no-repeat;
  background-attachment: scroll;
  background-position: center center;
  background-size: cover;
}
.masthead-subheading {
  font-size: 1.5rem;
  font-style: italic;
  line-height: 1.5rem;
  margin-bottom: 25px;
  font-family: "Roboto Slab", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
.text-uppercase {
  text-transform: uppercase !important;
}
</style>

