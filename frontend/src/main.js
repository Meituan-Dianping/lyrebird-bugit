import Vue from 'vue'
import App from './App.vue'
import store from './store/index'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import locale from 'view-design/dist/locale/en-US'
import io from 'socket.io-client'
import { bus } from './eventbus'

Vue.config.productionTip = false
Vue.use(ViewUI, { locale })
Vue.use(ViewUI)

Vue.prototype['$io'] = io()
Vue.prototype.$bus = bus

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
