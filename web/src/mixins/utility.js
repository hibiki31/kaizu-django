import Vue from 'vue'

Vue.mixin({
  methods: {
    $_sleep (msec) {
      return new Promise(resolve => setTimeout(resolve, msec))
    },
    $_convertNumFormat (num) {
      if (!num) {
        return 0
      } else if (num < 10000) {
        return num.toLocaleString()
      }
      const formatNum = String(num).slice(0, -3)
      return formatNum[0] + '.' + formatNum[1] + '万'
    },
    $_pushNotice (text, type, group = 'default') {
      this.$notify({
        group,
        text,
        type,
        duration: 5000
      })
    }
  }
})
