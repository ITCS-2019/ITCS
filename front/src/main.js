// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

// Components
import './components'

// Plugins
import './plugins'
window.axios = require('axios')
Vue.prototype.axios = window.axios
window.axios.defaults.headers.common['X-CSRFToken'] = `${gToken.token}`

import html2canvas from 'html2canvas'
window.html2canvas = html2canvas


// Sync router with store
import { sync } from 'vuex-router-sync'

// Application imports
import App from './App'
import i18n from '@/i18n'
import router from '@/router'
import store from '@/store'

import 'devextreme/dist/css/dx.common.css';
import 'devextreme/dist/css/dx.light.compact.css';

// Sync store with router
sync(store, router)

Vue.config.productionTip = false

// Components
Vue.component('DxGrid', require('@/components/devExtremeGrid/DxGrid.vue').default);

/* eslint-disable no-new */
window.vue = new Vue({
  i18n,
  router,
  store,
  render: h => h(App)
}).$mount('#app')
