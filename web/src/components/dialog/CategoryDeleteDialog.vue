<template>
<v-dialog
      v-model="dialogState"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          カテゴリを削除
        </v-card-title>
        <v-card-text>{{ item.name }}を削除します．関連するサブカテゴリ、トランザクション、アイテムすべてが消えます</v-card-text>
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
      deleteUrl: '',
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
    openDialog (item, mode) {
      if (mode === 'big') {
        this.deleteUrl = `/api/rest/categorys/${item.pk}/`
      } else {
        this.deleteUrl = `/api/rest/subcategorys/${item.pk}/`
      }
      this.item = item
      this.dialogState = true
    },
    runMethod () {
      axios.request({
        method: 'delete',
        url: this.deleteUrl,
        data: { id: this.item.id }
      })
        .then(res => {
          this.$_pushNotice('成功しました', 'success')
        })
        .catch(error => {
          this.$_pushNotice(error.response.data.detail, 'error')
        })
      this.dialogState = false
    }
  }
}
</script>
