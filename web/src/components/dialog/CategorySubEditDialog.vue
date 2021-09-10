<template>
<v-dialog width="320" v-model="dialogState">
    <v-card>
        <v-card-title>編集</v-card-title>
        <v-card-text>
            <v-text-field
                spellcheck="false"
                label="名前"
                placeholder=" "
                v-model="item.name"
            ></v-text-field>
            <v-text-field
                spellcheck="false"
                label="コード"
                placeholder=" "
                v-model="item.code"
            ></v-text-field>
            <v-select
            :items="categoryBig"
            item-text="code"
            item-value="id"
            label="カテゴリ"
            placeholder=" "
            v-model="item.categoryBigId"
          >
            <template v-slot:item="{ item }">
              <span v-bind:style="{ color: item.color }">{{ item.code }} - {{ item.name }}</span>
            </template>
            <template v-slot:selection="{ attr, on, item, selected }">
              <span v-text="item.name" v-bind="attr" :input-value="selected" v-on="on"></span>
            </template>
          </v-select>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="runMethod()">更新</v-btn>
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
        code: '',
        categoryBigId: ''
      },
      categoryBig: {}
    }
  },
  name: 'Home',
  methods: {
    openDialog (item, categoryBig) {
      console.log(categoryBig)
      this.item = item
      this.categoryBig = categoryBig
      this.dialogState = true
    },
    runMethod () {
      axios
        .put('/api/category/sub', this.item)
        .then((res) => {
          if (res.status !== 200) {
            this.$_pushNotice('処理に失敗しました', 'error')
            return
          }
          this.$_pushNotice('成功しました', 'success')
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
      this.dialogState = false
    }
  }
}
</script>
