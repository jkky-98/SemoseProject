<template>
  <div>
    <b-form v-if="show">
      <div class="white-box">
      <b-input-group 
        prepend="Address" 
        class="mt-3"
        id="input-group-1"
        label="Address"
        label-for="input-1"
      >
        <b-form-input v-model="dataAddress"></b-form-input>
          <b-input-group-append>
            <b-button variant="info" @click="execDaumPostcode()">주소입력</b-button>
          </b-input-group-append>
      </b-input-group>

      <b-form-group
        id="input-group-2"
        label="Store List"
        label-for="input-2"
        description="자주 이용하는 시설을 선택해주세요."
      >
        <b-form-select 
        id="input-2"
        v-model="selectedOption"
        :options="stores"
        @input="addToSelected"
        required
        >
        </b-form-select>
      </b-form-group>

      <b-card-group deck>
        <b-card
          header="수정을 원하시면 추가된 항목버튼을 클릭해주세요."
          header-tag="header"
          title="CHOOSED STORES"
        >
          <b-button
            v-for="item in selected_list"
            :key="item"
            variant="success"
            class="mr-2"
            @click="removeFromSelected(item)"
          >
            {{ item }}
          </b-button>
        </b-card>
      </b-card-group>

      <b-button variant="info" @click="updateStore">Submit</b-button>
      <b-button variant="danger" @click="resetSelected">Reset</b-button>
      </div>
    </b-form>
  </div>

</template>

<script>

  export default {
    name: 'FormComponent',
    data() {
      return {

        
        // daum post code data //
        postcode: "",
        dataAddress: "",
        extraAddress: "",
        // daum post code data //

        // select data //
        stores: [
          { text: 'Select', value: null },
          { text: '스타벅스', value: '스타벅스' },
          { text: '맥도날드', value: '맥도날드' },
          { text: '메가커피', value: '메가MGC커피' },
          { text: '편의점', value: '편의점' },
          { text: '올리브영', value: '올리브영' },
          { text: '슈퍼', value: '슈퍼' },
          { text: '코인노래방', value: '코인노래방' },
          { text: '필라테스', value: '필라테스' },
          { text: '헬스장', value: '헬스장' },
          { text: '은행', value: '은행' },
          { text: '스터디카페', value: '스터디카페' },
          { text: '인쇄', value: '인쇄' },
          { text: '공원', value: '공원' },
          { text: '약국', value: '약국' },
          { text: '내과', value: '내과' },
          { text: '한의원', value: '한의원' },
          { text: '우체국', value: '우체국' },
          { text: '배스킨라빈스', value: '배스킨라빈스' },
          { text: '교보문고', value: '교보문고' },
          { text: '아주대학교', value: '아주대학교' },

    
        ],
        selected: null,
        selected_list: [],
        selectedOption: null,
        // select data //

        show: true,
      }
    },
    methods: {

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
            this.$emit("onUpdateAddress", this.dataAddress);
          },
        }).open();
      },
      addToSelected() {
        if (!this.selected_list.includes(this.selectedOption)) {
        this.selected_list.push(this.selectedOption);
        }
      },
      removeFromSelected(item) {
        const index = this.selected_list.indexOf(item);
        if (index !== -1) {
          this.selected_list.splice(index, 1);
        }
      },
      resetSelected() {
      this.selected_list = [];
      },
      updateStore() {
        this.$emit("onUpdateStore", this.selected_list);
        this.resetSelected();
      },
  },
    props: {
    },
  }
</script>
<style>
.white-box {
  background-color: #f0f0f0;
  padding: 20px; /* 원하는 패딩을 적용합니다. */
  border: 1px solid #f0f0f0; /* 원하는 테두리 스타일을 적용합니다. */
  border-radius: 10px; /* 원하는 테두리 모서리를 적용합니다. */
  /* 기타 원하는 스타일을 적용할 수 있습니다. */
}
</style>