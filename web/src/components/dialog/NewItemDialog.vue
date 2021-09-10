<template>
<v-dialog width="800" v-model="dialogState">
      <v-card>
        <v-tabs v-model="tabId" background-color="secondary" dark>
          <v-tab>
            支出
          </v-tab>
          <v-tab>
            収入
          </v-tab>
          <v-tab>
            振替
          </v-tab>
        </v-tabs>
          <v-container>
            <!-- トランザクション行 -->
            <v-row>
              <v-col cols="12" sm="12" md="3">
                <v-text-field
                  spellcheck="false"
                  label="日付"
                  type="date"
                  placeholder=" "
                  v-model="item.date"
                  :rules="[required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="2" v-if="tabId != 1">
                <v-select
                  :items="walletList"
                  v-model="item.walletExpensesId"
                  label="出金口座"
                  item-text="code"
                  item-value="id"
                  placeholder=" "
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
              <v-col cols="12" sm="12" md="2" v-if="tabId != 0">
                <v-select
                  :items="walletList"
                  v-model="item.walletIncomeId"
                  label="入金口座"
                  item-text="code"
                  item-value="id"
                  item-color="color"
                  placeholder=" "
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
               <v-col cols="12" sm="10" md="5">
              <v-autocomplete
                v-model="item.shop"
                v-bind:options="options"
                :items="shopList"
                :loading="isLoading"
                :search-input.sync="search"
                item-text="shop"
                item-value="shop"
                label="店名"
                placeholder=" "
                return-object
                no-filter
                :rules="[required]"
              >
                <template v-slot:item="{ item }">
                  <v-row>
                    <v-col cols="12" sm="9">
                      <span>{{ item.shop }}</span>
                    </v-col>
                    <v-col cols="12" sm="3">
                      <span>{{ item.count }} 回</span>
                    </v-col>
                  </v-row>

                </template>
              </v-autocomplete>
              </v-col>
            </v-row>
            <!-- アイテム行 -->
            <v-row v-for="(row,index) in item.items" :key="index">
              <v-col cols="12" sm="12" md="2">
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
              <v-col cols="12" sm="12" md="2">
                <v-select
                :items="subCategory"
                item-text="name"
                item-value="id"
                label="サブカテゴリ"
                placeholder=" "
                no-data-text="サブカテゴリが存在しません"
                v-model="row.categorySubId"
                :rules="[required]"
                >
                </v-select>
              </v-col>
              <v-col cols="12" sm="10" md="6">
                <v-text-field

                  label="品目"
                  placeholder=" "
                  v-model="row.name"
                  :rules="[required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="2" md="2">
                <vuetify-money
                  v-model="row.amount"
                  label="金額"
                  placeholder=" "
                  v-bind:options="options"
                  :rules="[required]"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-btn class="ml-3" @click="addItem">+</v-btn>
            </v-row>
          </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn v-if="this.mode==='post'" color="blue darken-1" text @click="runPostMethod()">新規</v-btn>
          <v-btn v-if="this.mode==='copy'" color="blue darken-1" text @click="runPostMethod()">複製</v-btn>
          <v-btn v-if="this.mode==='put'" color="blue darken-1" text @click="runPutMethod()">編集</v-btn>
        </v-card-actions>
      </v-card>
</v-dialog>
</template>

<script>
import axios from '@/axios/index'
import moment from 'moment'
export default {
  name: 'Home',
  data: function () {
    return {
      // 状態管理
      dialogState: false,
      search: null,
      isLoading: false,
      tabId: null,
      mode: 'new',
      // 親からの参照渡し
      itemsLsit: [],
      // フォームリスト
      bigCategorySelect: 0,
      bigCategory: [],
      subCategory: [],
      walletList: [],
      shopList: [],
      // フォームアイテム
      item: {
        date: '',
        shop: '',
        walletExpensesId: 0,
        walletIncomeId: 0,
        provider: '',
        providerId: 0,
        items: [
          {
            name: '',
            kind: '',
            amount: '',
            categorySubId: '',
            transactionId: 0
          }
        ]
      },
      headers: [
        { text: 'date' },
        { text: 'big' },
        { text: 'sub' },
        { text: 'name' },
        { text: 'shop' },
        { text: 'expenses' },
        { text: 'kind' },
        { text: 'income' },
        { text: 'amount' },
        { text: 'actions' }
      ],
      options: {
        locale: 'ja',
        prefix: '',
        suffix: '',
        length: 11,
        precision: 0
      }
    }
  },
  filters: {
    moment (value, format) {
      return moment(value).format(format)
    },
    yen (value) {
      return value.toLocaleString()
    }
  },
  watch: {
    search (val) {
      if (this.isLoading) return
      this.isLoading = true
      axios
        .get('/api/transaction/shop', { params: { shopSearch: val } })
        .then((response) => {
          this.shopList = response.data
          this.isLoading = false
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  },
  methods: {
    required: (value) => !!value || '必須',
    openDialog () {
      this.mode = 'post'
      this.dialogState = true
      this.item = {
        date: '',
        shop: '',
        walletExpensesId: 0,
        walletIncomeId: 0,
        provider: '',
        providerId: 0,
        items: [{
          name: '',
          kind: '',
          amount: '',
          categoryBigId: '',
          categorySubId: '',
          transactionId: 0
        }]
      }
    },
    addItem () {
      this.item.items.push({
        date: '',
        shop: '',
        walletExpensesId: 0,
        walletIncomeId: 0,
        provider: '',
        providerId: 0,
        items: [{
          name: '',
          kind: '',
          amount: '',
          categorySubId: '',
          categoryBigId: '',
          transactionId: 0
        }]
      })
    },
    openEditDialog (item) {
      this.mode = 'put'
      this.dialogState = true
      this.inputValueMapping(item)
    },
    openCopyDialog (item) {
      this.mode = 'copy'
      this.dialogState = true
      this.inputValueMapping(item)
    },
    inputValueMapping (item) {
      // タブIDと種別をマッピング
      if (item.kind === 'expenses') {
        this.tabId = 0
      } else if (item.kind === 'income') {
        this.tabId = 1
      } else if (item.kind === 'transfer') {
        this.tabId = 2
      }
      // 取引先とカテゴリの選択肢を予め用意
      this.shopList = [item.shop]
      this.bigCategorySelect = item.categoryBigId
      this.getSubCategory(item.categoryBigId)
      // アイテムをマッピング
      this.item = {
        id: item.transactionId,
        date: moment(item.date).format('YYYY-MM-DD'),
        shop: { shop: item.shop },
        walletExpensesId: item.walletExpensesId,
        walletIncomeId: item.walletIncomeId,
        provider: '',
        providerId: 0,
        items: [{
          id: item.id,
          name: item.name,
          kind: item.kind,
          amount: item.amount,
          categorySubId: item.categorySubId,
          transactionId: 0
        }]
      }
    },
    postValueMapping () {
      this.dialogState = false
      this.item.shop = this.item.shop.shop
      this.item.date = moment(this.item.date).format()
      if (this.tabId === 0) {
        this.item.walletIncomeId = this.item.walletExpensesId
      } else if (this.tabId === 1) {
        this.item.walletExpensesId = this.item.walletIncomeId
      }
      for (const row in this.item.items) {
        if (this.tabId === 0) {
          this.item.items[row].kind = 'expenses'
        } else if (this.tabId === 1) {
          this.item.items[row].kind = 'income'
        } else if (this.tabId === 2) {
          this.item.items[row].kind = 'transfer'
        }
      }
      this.item.walletIncomeI = this.item.walletExpensesId
      console.log(this.item)
    },
    runPostMethod () {
      this.postValueMapping()
      axios
        .post('/api/transaction/items', this.item)
        .then((res) => {
          this.$_pushNotice('成功しました', 'success')
          this.$emit('reload')
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
    },
    runPutMethod () {
      this.postValueMapping()
      axios
        .put('/api/transaction/items', this.item)
        .then((res) => {
          this.$_pushNotice('成功しました', 'success')
          this.$emit('reload')
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
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
  },
  mounted: async function () {
    axios
      .get('/api/wallet')
      .then((response) => {
        this.walletList = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
    axios
      .get('/api/category/big')
      .then((response) => {
        this.bigCategory = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
    axios
      .get('/api/transaction/shop')
      .then((response) => {
        this.shopList = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
  }
}
</script>
