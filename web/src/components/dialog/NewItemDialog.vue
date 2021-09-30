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
                  v-model="transaction.date"
                  :rules="[required]"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="12" md="2" v-if="tabId != 1">
                <v-select
                  :items="walletList"
                  v-model="transaction.wallet_expenses_id"
                  label="出金口座"
                  item-text="code"
                  item-value="pk"
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
                  v-model="transaction.wallet_income_id"
                  label="入金口座"
                  item-text="code"
                  item-value="pk"
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
                 <v-combobox
                 v-model="transaction.supplier_id"
                  :items="shopList"
                  label="取引先"
                  item-text="name"
                ></v-combobox>
              </v-col>
            </v-row>
            <!-- アイテム行 -->
            <v-row v-for="(row,index) in transaction.items" :key="index">
              <v-col cols="12" sm="12" md="2">
                <v-select
                :items="bigCategory"
                item-text="code"
                item-value="pk"
                label="カテゴリ"
                placeholder=" "
                v-model="row.bigCategorySelect"
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
                :items="getSubCategory(row.bigCategorySelect)"
                item-text="name"
                item-value="pk"
                label="サブカテゴリ"
                placeholder=" "
                no-data-text="サブカテゴリが存在しません"
                v-model="row.sub_category_id"
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
      transaction: {
        date: null,
        supplier_id: null,
        wallet_income_id: 0,
        wallet_expenses_id: 0,
        kind: null,
        items: [
          {
            name: '',
            amount_income: 0,
            amount_expenses: 0,
            sub_category_id: 0
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
        .get('/api/rest/suppliers', { params: { name: val } })
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
      this.transaction.items.push({
        name: '',
        amount_income: 0,
        amount_expenses: 0,
        sub_category_id: 0
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
    inputValueMapping (transaction) {
      // タブIDと種別をマッピング
      if (transaction.kind === 'expenses') {
        this.tabId = 0
      } else if (transaction.kind === 'income') {
        this.tabId = 1
      } else if (transaction.kind === 'transfer') {
        this.tabId = 2
      }
      // アイテムをマッピング
      this.transaction = {
        pk: transaction.pk,
        date: moment(transaction.date).format('YYYY-MM-DD'),
        supplier_id: transaction.supplier.name,
        wallet_income_id: transaction.wallet_income.pk,
        wallet_expenses_id: transaction.wallet_expenses.pk,
        items: []
      }
      for (const i in transaction.items) {
        this.transaction.items.push({
          name: transaction.items[i].name,
          amount: transaction.kind === 'income' ? transaction.items[i].amount_income : transaction.items[i].amount_expenses,
          sub_category_id: transaction.items[i].sub_category.pk,
          bigCategorySelect: transaction.items[i].sub_category.category.pk
        })
      }
    },
    async postValueMapping () {
      this.dialogState = false
      this.transaction.date = moment.utc(this.transaction.date).format()
      if (this.shopList.find(shop => shop.name === this.transaction.supplier_id)) {
        this.transaction.supplier_id = this.shopList.find(shop => shop.name === this.transaction.supplier_id).pk
      } else if (typeof (this.transaction.supplier_id) === 'string' || this.transaction.supplier_id instanceof String) {
        await axios
          .post('/api/rest/suppliers/', { name: this.transaction.supplier_id })
          .then((res) => {
            this.transaction.supplier_id = res.data.pk
          })
      } else {
        this.transaction.supplier_id = this.transaction.supplier_id.pk
      }
      // 種別のマッピング
      if (this.tabId === 0) {
        this.transaction.kind = 'expenses'
        this.transaction.wallet_income_id = this.transaction.wallet_expenses_id
      } else if (this.tabId === 1) {
        this.transaction.kind = 'income'
        this.transaction.wallet_expenses_id = this.transaction.wallet_income_id
      } else if (this.tabId === 2) {
        this.transaction.kind = 'transfer'
      }
      for (const i in this.transaction.items) {
        // 金額のマッピング
        if (this.tabId === 0) {
          this.transaction.items[i].amount_income = 0
          this.transaction.items[i].amount_expenses = this.transaction.items[i].amount
        } else if (this.tabId === 1) {
          this.transaction.items[i].amount_income = this.transaction.items[i].amount
          this.transaction.items[i].amount_expenses = 0
        } else if (this.tabId === 2) {
          this.transaction.items[i].amount_income = this.transaction.items[i].amount
          this.transaction.items[i].amount_expenses = this.transaction.items[i].amount
        }
      }
      console.log(this.transaction)
    },
    async runPostMethod () {
      await this.postValueMapping()
      axios
        .post('/api/rest/transactions/', this.transaction)
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
      for (const i in this.bigCategory) {
        if (this.bigCategory[i].pk === bigId) {
          return this.bigCategory[i].sub_category
        }
      }
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
        this.bigCategory = response.data
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
