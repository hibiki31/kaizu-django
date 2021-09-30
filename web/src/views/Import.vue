<template>
  <div class="itemList">
    <v-card>
      <form>
        <v-select
          :items="walletList"
          v-model="wallet"
          label="入金口座"
          item-text="code"
          item-value="pk"
          placeholder=" "
        >
          <template v-slot:item="{ item }">
            <span v-bind:style="{ color: item.color }">{{ item.code }} - {{ item.name }}</span>
          </template>
          <template v-slot:selection="{ attr, on, item, selected }">
            <span v-text="item.name" v-bind="attr" :input-value="selected" v-on="on"></span>
          </template>
        </v-select>
        <v-select
          :items="categoryList"
          item-text="code"
          item-value="pk"
          label="カテゴリ"
          placeholder=" "
          v-model="category"
        >
          <template v-slot:item="{ item }">
            <span v-bind:style="{ color: item.color }"
              >{{ item.code }} - {{ item.name }}</span
            >
          </template>
          <template v-slot:selection="{ attr, on, item, selected }">
            <span
              v-text="item.name"
              v-bind="attr"
              :input-value="selected"
              v-on="on"
            ></span>
          </template>
        </v-select>
        <v-select
          :items="getSubCategory(this.category)"
          item-text="name"
          item-value="pk"
          label="サブカテゴリ"
          placeholder=" "
          no-data-text="サブカテゴリが存在しません"
          v-model="subcategory"
        >
        </v-select>
        <v-combobox
          v-model="supplier"
          :items="shopList"
          label="取引先"
          item-text="name"
        ></v-combobox>
        <v-file-input v-model="file">
          <template v-slot:append-outer>
            <v-btn height="32" :disabled="!file" @click="upload">Upload</v-btn>
          </template>
        </v-file-input>
      </form>
    </v-card>
  </div>
</template>

<script>
import FormData from 'form-data'
import axios from '@/axios/index'

export default {
  name: 'Import',
  components: {},
  data: function () {
    return {
      file: null,
      fileData: null,
      wallet: null,
      subcategory: null,
      supplier: null,
      shopList: [],
      category: null,
      categoryList: [],
      walletList: []
    }
  },
  methods: {
    getSubCategory (id) {
      for (const i in this.categoryList) {
        if (this.categoryList[i].pk === id) {
          return this.categoryList[i].sub_category
        }
      }
    },
    async upload () {
      // ショップの追加をするか処理
      if (this.shopList.find((shop) => shop.name === this.supplier)) {
        this.supplier = this.shopList.find(
          (shop) => shop.name === this.supplier
        ).pk
      } else if (typeof this.supplier === 'string' || this.supplier instanceof String) {
        await axios
          .post('/api/rest/suppliers/', { name: this.supplier })
          .then((res) => {
            this.supplier = res.data.pk
          })
      } else {
        this.supplier = this.supplier.pk
      }

      const formData = new FormData()
      formData.append('file', this.file)
      formData.append('type', 'rakuten')
      formData.append('wallet', this.wallet)
      formData.append('subcategory', this.subcategory)
      formData.append('supplier', this.supplier)

      const res = await axios.post(
        '/api/transaction/import/rakuten_card',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )

      console.log(res)
    }
  },
  mounted: async function () {
    axios
      .get('/api/rest/wallets')
      .then((response) => {
        this.walletList = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
    axios
      .get('/api/rest/categorys')
      .then((response) => {
        this.categoryList = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
    axios
      .get('/api/rest/suppliers')
      .then((response) => {
        this.shopList = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
  }
}
</script>
