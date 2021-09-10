<template>
  <div class="itemList">
    <!-- ダイアログコンポーネント -->
    <NewItemDialogComponents ref="newDialog" @reload='this.getItemList'/>
    <TransactionDeleteDialogComponents ref="deleteDialog" @reload='this.getItemList'/>
    <v-card class="mb-2">
      <!-- カード上部アクションエリア -->
      <v-card-actions>
        <!-- 追加ボタン -->
        <v-btn
          v-on:click="openNewDialog()"
          icon
        >
          <v-icon left>mdi-plus</v-icon>
        </v-btn>
        <!-- 種別フィルタ -->
        <v-select
          :items="kindList"
          v-model="itemQuery.kind"
          class="pl-3"
          label="種別"
          item-text="name"
          item-value="key"
          placeholder=" "
        >
        </v-select>
        <!-- 口座フィルター -->
        <v-select
          :items="walletList"
          v-model="itemQuery.walletId"
          class="pl-3"
          label="口座"
          item-text="name"
          item-value="id"
          item-color="color"
          placeholder=" "
        >
          <template v-slot:item="{ item }">
            <span v-bind:style="{ color: item.color }">{{ item.name }}</span>
          </template>
        </v-select>
        <!-- カテゴリフィルター -->
        <v-select
          :items="bigCategory"
          item-text="code"
          item-value="id"
          label="カテゴリ"
          placeholder=" "
          class="pl-3"
          v-model="itemQuery.categoryBigId"
          v-on:change="getSubCategory"
        >
          <template v-slot:item="{ item }">
            <span v-bind:style="{ color: item.color }">{{ item.code }} - {{ item.name }}</span>
          </template>
          <template v-slot:selection="{ attr, on, item, selected }">
            <span v-text="item.name" v-bind="attr" :input-value="selected" v-on="on"></span>
          </template>
        </v-select>
        <!-- サブカテゴリフィルター -->
        <v-select
        :items="subCategory"
        item-text="name"
        class="pl-3"
        item-value="id"
        placeholder=" "
        label="サブカテゴリ"
        v-model="itemQuery.categorySubId"
        >
        </v-select>
        <!-- 項目名フィルター -->
        <v-text-field
          class="pl-3"
          label="項目名"
          placeholder=" "
          v-model="itemQuery.nameSearch"
        ></v-text-field>

        <v-text-field
          class="pl-3"
          label="取引先"
          placeholder=" "
          v-model="itemQuery.shopSearch"
        ></v-text-field>
        <v-btn icon @click="clearFilter">
          <v-icon>mdi-eraser</v-icon>
        </v-btn>
        <v-btn icon
          v-on:click="this.clickSearchButton"
          :loading="loadingApi"
          :disabled="loadingApi"
        >
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </v-card-actions>
      <v-data-table
        hidden
        :dense="true"
        :headers="headers"
        :items="itemsList"
        :items-per-page="15"
        :footer-props="{
          'items-per-page-options': [15, 30],
          showFirstLastPage: true,
        }"
        :disable-sort="true"
        :options.sync="options"
        :server-items-length="totalItems"
        :loading="loadingApi"
        loading-text="Now loading!!"
        multi-sort
      >
        <template v-slot:item="{ item }" justify="right">
          <tr>
            <td>
              <div small v-bind:class="['no-wrap', 'px-1']">{{ item.date | moment("YYYY-MM-DD") }}</div>
            </td>
            <!-- カテゴリ -->
            <td>
              <v-chip label small
                v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1', ]"
                v-bind:style="{ background: item.categoryBigColor }"
              >
                {{ item.categoryBigName }}
              </v-chip>
            </td>
            <td>
              <span class='caption font-weight-bold no-wrap px-1'>{{ item.categorySubName }}</span>
            </td>
            <!-- 名目 -->
            <td>{{ item.name }}</td>
            <!-- 取引先 -->
            <td>{{ item.shop }}</td>
            <td>
              <v-chip v-if="item.kind == 'expenses' || item.kind == 'transfer'" label x-small
                v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1',]"
                v-bind:style="{ background: item.walletExpensesColor }"
              >
                {{ item.walletExpensesName }}
              </v-chip>
            </td>
            <td>
              <v-icon v-if="item.kind == 'expenses'" color="red darken-1">mdi-chevron-double-right</v-icon>
              <v-icon v-else-if="item.kind == 'income'" color="blue">mdi-chevron-double-right</v-icon>
              <v-icon v-else-if="item.kind == 'transfer'" color="green">mdi-chevron-double-right</v-icon>
            </td>
            <td>
              <v-chip v-if="item.kind == 'income' || item.kind == 'transfer'" label x-small
                v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1',]"
                v-bind:style="{ background: item.walletIncomeColor }"
              >
                {{ item.walletIncomeName }}
              </v-chip>
            </td>
            <td class="no-wrap text-right">¥ {{ item.amount | yen() }}</td>
            <td>
              <v-icon small class="mr-2" @click="openEditDialog(item)">
                mdi-pencil
              </v-icon>
              <v-icon small class="mr-2" @click="openCopyDialog(item)">
                mdi-content-copy
              </v-icon>
              <v-icon small @click="openDeleteDialog(item)">
                mdi-delete
              </v-icon>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <v-card v-for="item in itemsList" :key="item.id" class="pa-1 mb-2">
      <div>
        <span small v-bind:class="['no-wrap', 'px-1', 'font-weight-bold']" style="display: inline-block;width: 130px;">{{ item.date | moment("YYYY-MM-DD") }}</span>
        <span :style="{display: 'inline-block', width: '140px'}">
        <v-chip label small
          v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1', ]"
          v-bind:style="{ background: item.categoryBigColor}"
        >
          {{ item.categoryBigName }}
        </v-chip>
        <span class='caption font-weight-bold no-wrap px-1'>{{ item.categorySubName }}</span>
        </span>
        <span :style="{display: 'inline-block', width: '90px'}">
        <v-chip v-if="item.kind == 'expenses' || item.kind == 'transfer'" label small
          v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1',]"
          v-bind:style="{ background: item.walletExpensesColor}"
        >
          {{ item.walletExpensesName }}
        </v-chip>
        </span>
        <v-icon v-if="item.kind == 'expenses'" color="red darken-1">mdi-chevron-double-right</v-icon>
        <v-icon v-else-if="item.kind == 'income'" color="blue">mdi-chevron-double-right</v-icon>
        <v-icon v-else-if="item.kind == 'transfer'" color="green">mdi-chevron-double-right</v-icon>
        <span :style="{display: 'inline-block', width: '90px'}">
          <v-chip v-if="item.kind == 'income' || item.kind == 'transfer'" label small
            v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1',]"
            v-bind:style="{ background: item.walletIncomeColor }"
          >
            {{ item.walletIncomeName }}
          </v-chip>
        </span>
        <span class="no-wrap text-right mr-2 font-weight-bold" :style="{display: 'inline-block', width: '80px'}">¥ {{ item.amount | yen() }}</span>
        <v-icon small class="mr-2" @click="openEditDialog(item)">
          mdi-pencil
        </v-icon>
        <v-icon small class="mr-2" @click="openCopyDialog(item)">
          mdi-content-copy
        </v-icon>
        <v-icon small @click="openDeleteDialog(item)">
          mdi-delete
        </v-icon>
        <span class="caption" :style="{display: 'inline-block', }">{{ item.shop }}</span>
      </div>
      <span class="caption">{{ item.name }}</span>
    </v-card>
    <v-card>
      <v-pagination
      v-model="page"
      :length="Math.ceil(totalItems/10)"
      :total-visible="7"
    ></v-pagination>
    </v-card>
  </div>
</template>

<script>
import axios from '@/axios/index'
import moment from 'moment'
import NewItemDialogComponents from '../components/dialog/NewItemDialog'
import TransactionDeleteDialogComponents from '../components/dialog/TransactionDeleteDialog'

export default {
  name: 'Home',
  components: {
    NewItemDialogComponents,
    TransactionDeleteDialogComponents
  },
  data: function () {
    return {
      page: 1,
      // 状態管理
      loadingApi: false,
      // 検索用クエリ
      itemQuery: {
        nameSearch: '',
        startDate: '2000-01-01',
        endDate: '2100-01-01'
      },
      // サーバサイドページング用
      totalItems: -1,
      options: {},
      // リスト
      bigCategory: [],
      subCategory: [],
      itemsList: [],
      walletList: [],
      kindList: [
        { key: 'expenses', name: '支出' },
        { key: 'income', name: '収入' },
        { key: 'transfer', name: '振替' }
      ],
      // テーブル用
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
      ]
    }
  },
  watch: {
    options: {
      handler () {
        window.scrollTo({ top: 0, behavior: 'smooth' })
        this.itemQuery.offset = this.options.itemsPerPage * (this.options.page - 1)
        this.itemQuery.limit = this.options.itemsPerPage
        this.getItemList()
      },
      deep: true
    },
    page: {
      handler () {
        window.scrollTo({ top: 0, behavior: 'smooth' })
        this.itemQuery.offset = 10 * (this.page - 1)
        this.itemQuery.limit = 10
        this.getItemList()
      },
      deep: true
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
  methods: {
    clearFilter () {
      this.itemQuery = { startDate: '2000-01-01', endDate: '2100-01-01' }
    },
    // ダイアログ系
    openNewDialog () {
      this.$refs.newDialog.openDialog(this.itemsList)
    },
    openDeleteDialog (item) {
      this.$refs.deleteDialog.openDialog(item)
    },
    openEditDialog (item) {
      this.$refs.newDialog.openEditDialog(item)
    },
    openCopyDialog (item) {
      this.$refs.newDialog.openCopyDialog(item)
    },
    // カテゴリに連動してサブカテゴリ更新
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
          }
        })
    },
    clickSearchButton () {
      this.itemQuery.offset = 0
      this.getItemList()
    },
    // アイテム更新,検索用クエリから
    getItemList () {
      this.itemQuery.limit = 10
      this.loadingApi = true
      axios
        .get('/api/item', { params: this.itemQuery })
        .then((response) => {
          this.totalItems = response.data.length
          this.itemsList = response.data.items
          this.loadingApi = false
        })
    }
  },
  // 起動時にデータ取得
  // tableのoptionを監視していると起動時に一度itemを取得するのでここでやってない
  mounted: async function () {
    // routeのGETクエリは読み取り専用なので最初に取得して以後は使わない
    this.itemQuery = this.$route.query
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
  }
}
</script>

<style>
.no-wrap {
  white-space: nowrap;
}
</style>
