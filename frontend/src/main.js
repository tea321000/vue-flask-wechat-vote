import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
import './permission'
import Cookies from 'js-cookie'
import Element from 'element-ui'
//引入ECHARTS
import ECharts from 'vue-echarts' // 在 webpack 环境下指向 components/ECharts.vue
import 'echarts/lib/chart/pie'
Vue.component('v-chart', ECharts)
//引入QRCODE
import VueQrcode from '@chenfengyuan/vue-qrcode';
Vue.component(VueQrcode.name, VueQrcode);


Vue.config.productionTip = false

Vue.use(Element, {
  size: Cookies.get('size') || 'medium', // 设置element-ui默认大小
  i18n: (key, value) => i18n.t(key, value)
})



new Vue({
  router,
  store,
  render: function (h) {
    return h(App)
  }
}).$mount('#app')