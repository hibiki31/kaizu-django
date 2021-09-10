<template>
<v-dialog
      v-model="dialogState"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          取引を削除
        </v-card-title>
        <v-card-text>削除します．</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialogState = false"
          >
            キャンセル
          </v-btn>
          <v-btn
            color="red darken-1"
            text
            @click="runMethod()"
          >
            削除
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import axios from '@/axios/index'

export default {
  data: function () {
    return {
      dialogState: false,
      item: {
        id: '',
        name: '',
        color: '',
        code: ''
      }
    }
  },
  name: 'Home',
  methods: {
    openDialog (item) {
      this.item = item
      this.dialogState = true
    },
    runMethod () {
      this.dialogState = false
      axios.request({
        method: 'delete',
        url: '/api/transaction',
        data: { id: this.item.id }
      })
        .then(res => {
          this.$emit('reload')
          this.$_pushNotice('成功しました', 'success')
        })
        .catch(error => {
          this.$_pushNotice(error.response.data.detail, 'error')
        })
    }
  }
}
</script>
