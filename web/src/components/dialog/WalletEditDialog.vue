<template>
<v-dialog width="680" v-model="dialogState">
    <v-card>
        <v-card-title>編集</v-card-title>
        <v-card-text>

          <v-container>
            <v-row>
            <v-col cols="12" sm="12" md="6">
            <v-text-field
                spellcheck="false"
                label="名前"
                placeholder=" "
                v-model="item.name"
            ></v-text-field>
            <v-text-field
                spellcheck="false"
                label="種類"
                placeholder=" "
                v-model="item.kind"
            ></v-text-field>
            <v-text-field
                spellcheck="false"
                label="コード"
                placeholder=" "
                v-model="item.code"
            ></v-text-field>
            <v-text-field
                spellcheck="false"
                label="残高"
                placeholder=" "
                v-model="item.amount"
            ></v-text-field>
            <v-switch
              v-model="item.is_favorite"
              label="Favorite"
            ></v-switch>
            <v-switch
              v-model="item.is_hide"
              label="Hide"
            ></v-switch>
            </v-col>
            <v-col cols="12" sm="12" md="6">
                <v-color-picker
                v-model="item.color"
                show-swatches
                mode="hexa"
                hide-mode-switch
                ></v-color-picker>
            </v-col>
            </v-row>
            </v-container>
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
        pk: '',
        name: '',
        color: '',
        code: '',
        amount: 0,
        amount_sum: 0,
        kind: '',
        is_favorite: false,
        is_hide: true
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
      axios
        .put(`/api/rest/wallets/${this.item.pk}/`, this.item)
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
