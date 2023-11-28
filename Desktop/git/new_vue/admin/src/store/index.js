import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    address: "", // 주소 상태 초기값
    buttons: [], // 선택된 버튼 상태 초기값
    zickbang_point: [], // 직방 매물 선택 초기값
    receivedData: {},
  },
  getters: {
    getAddress: (state) => state.address,
    getSelectedButtons: (state) => state.buttons,
    getZickbangPoint: (state) => state.zickbang_point,
    getReceivedData: (state) => state.receivedData,
  },
  mutations: {
    SET_ZICKBANG_POINT(state, lat_lng) {
      state.zickbang_point = lat_lng;
    },
    SET_DEFAULT_BUTTONS(state, defaultButtons) {
      if (state.buttons.length === 0) {
        state.buttons = defaultButtons;
      }
    },
    SET_ADDRESS(state, address) {
      state.address = address;
    },
    SET_SELECTED_BUTTONS(state, buttons) {
      state.buttons = buttons;
    },
    SET_RECEIVED_DATA(state, receivedData) {
      state.receivedData = receivedData;
    },
  },
  actions: {
    saveAddress({ commit }, address) {
      commit("SET_ADDRESS", address);
    },
    clearAddress({ commit }) {
      commit("SET_ADDRESS", "");
    },
    setSelectedButtons({ commit }, buttons) {
      commit("SET_SELECTED_BUTTONS", buttons);
    },
    saveZickbangPoint({ commit }, lat_lng) {
      commit("SET_ZICKBANG_POINT", lat_lng);
    },
    clearZickbangPoint({ commit }) {
      commit("SET_ZICKBANG_POINT", []);
    },
    setReceivedData({ commit }, receivedData) {
      commit("SET_RECEIVED_DATA", receivedData); // mutation을 호출하여 상태 변수 업데이트하는 action
    },
  },
  modules: {},
});
