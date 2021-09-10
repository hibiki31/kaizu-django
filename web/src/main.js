import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'

import './mixins/utility'

import Notifications from 'vue-notification'
import velocity from 'velocity-animate'
import './plugins/vuetify-money.js'

import './registerServiceWorker'

Vue.config.productionTip = false
Vue.use(Notifications, { velocity })

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
