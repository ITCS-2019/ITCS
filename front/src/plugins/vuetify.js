import Vue from 'vue'
import Vuetify from 'vuetify'
import en from 'vuetify/es5/locale/en'
import uk from 'vuetify/es5/locale/uk'
import { Ripple } from 'vuetify/lib/directives'
import theme from './theme'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify, {
  lang: {
    locales: { en, uk },
    current: 'uk'
  },
  iconfont: 'mdi',
  theme,
  directives: {
    Ripple
  }
})
