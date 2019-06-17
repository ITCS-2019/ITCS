import Vue from 'vue'
import Vuetify from 'vuetify'
import { Ripple } from 'vuetify/lib/directives'
import theme from './theme'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify, {
  iconfont: 'mdi',
  theme,
  directives: {
    Ripple
  }
})
