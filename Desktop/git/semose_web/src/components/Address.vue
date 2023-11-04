<template>
  <div>
    <b-form-input v-model="inputaddress" 
    placeholder="주소를 입력하세요." >
    </b-form-input>
    <b-col class="pb-2" >
      <b-button size="lg" 
      @click='transferEvent'
      > 주소입력 완료
      </b-button>
    </b-col>

  </div>
</template>

<script>
export default {
  name: 'AddressComponent',
  props: {

  },
  data() {
    return {
      inputaddress: '' // 로컬 데이터로 사용할 변수
    }
  },
  methods: {
    transferEvent: function() {
      console.log('updateAddress')
      this.$emit('onUpdateAddress',this.inputaddress); // input 이벤트를 이용하여 주소를 부모 컴포넌트로 전달
    }
  }
}
</script>


<style>
</style>

