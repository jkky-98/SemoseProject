import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify, {
  theme: {
    dark: "#491D8F",
  },
});

export default new Vuetify({
  theme: { dark: true },
});
