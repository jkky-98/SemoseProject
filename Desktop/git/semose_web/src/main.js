import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import BootstrapVue3 from 'bootstrap-vue-3'
import router from './router'
import '@coreui/coreui/dist/css/coreui.min.css'


createApp(App).use(router).use(BootstrapVue3).mount('#app')

