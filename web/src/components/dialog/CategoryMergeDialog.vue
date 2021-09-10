<template>
<v-dialog
      v-model="dialogState"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
          カテゴリをマージ
        </v-card-title>
        <v-card-text>
          {{ item.name }}を
          <v-row>
              <v-col cols="12" sm="12" md="6">
                <v-select
                :items="bigCategory"
                item-text="code"
                item-value="id"
                label="カテゴリ"
                placeholder=" "
                v-on:change="getSubCategory"
                v-model="bigCategorySelect"
                :rules="[required]"
                >
                  <template v-slot:item="{ item }">
                    <span v-bind:style="{ color: item.color }">{{ item.code }} - {{ item.name }}</span>
                  </template>
                  <template v-slot:selection="{ attr, on, item, selected }">
                    <span v-text="item.name" v-bind="attr" :input-value="selected" v-on="on"></span>
                  </template>
                </v-select>
              </v-col>
              <v-col cols="12" sm="12" md="6">
                <v-select
                :items="subCategory"
                item-text="name"
                item-value="id"
                label="サブカテゴリ"
                placeholder=" "
                no-data-text="サブカテゴリが存在しません"
                v-model="subCategorySelect"
                :rules="[required]"
                >
                </v-select>
              </v-col>
          </v-row>
          にマージします.
          </v-card-text>
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
            マージ
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
      bigCategorySelect: 0,
      subCategorySelect: 0,
      bigCategory: [],
      subCategory: [],
      item: {
        id: '',
        name: ''
      }
    }
  },
  name: 'Home',
  methods: {
    required: (value) => !!value || '必須',
    openDialog (item, bigCategory) {
      this.bigCategory = bigCategory
      this.item = item
      this.dialogState = true
    },
    runMethod () {
      axios
        .put('/api/category/sub/merge', { mergeId: this.item.id, intoId: this.subCategorySelect })
        .then((res) => {
          this.$_pushNotice(res.data.length + '個のアイテムをマージ完了', 'success')
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
      this.dialogState = false
    },
    getSubCategory (bigId) {
      axios
        .get('/api/category/sub', {
          params: {
            bigId: bigId
          }
        })
        .then((response) => {
          if (response.status === 200) {
            this.subCategory = response.data
          } else {
            this.$_pushNotice('サーバーエラーが発生しました', 'error')
          }
        })
    }
  }
}
</script>
