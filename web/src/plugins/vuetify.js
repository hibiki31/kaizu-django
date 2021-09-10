import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#9FC9DD',
        secondary: '#392A59',
        accent: '#8C0B0B',
        error: '#E53935',
        warning: '#FBC02D',
        info: '#0288D1',
        success: '#00796B'
      }
    }
  }
})
