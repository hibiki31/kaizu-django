<template>
  <div class="home">
    <WalletEditDialog ref="walletEdit" />
    <WalletDeleteDialog ref="walletDelete" @reload='this.reload'/>
    <v-card>
      <v-btn class="ma-2" dark small color="accent" @click="this.favoriteFilter">
        <v-icon dark>mdi-heart</v-icon>
      </v-btn>
      <v-btn class="ma-2" dark small color="primary" @click="this.reload">
        <v-icon dark>mdi-cached</v-icon>
      </v-btn>
     <v-data-table
        :dense="true"
        :headers="headers"
        :items="walletsFavorite"
        :items-per-page="30"
        :footer-props="{
          'items-per-page-options': [10, 30],
          showFirstLastPage: true,
        }"
        :disable-sort="true"
      >
        <!-- 行 -->
        <template v-slot:item="{ item }" justify="right">
          <tr>
            <td>
              <v-chip label small
              :to="{ path: '/', query: { walletId: item.id }}"
              :class="['font-weight-bold', 'no-wrap', 'px-1', ]"
              :style="{ background: item.color }"
              >
              {{ item.name }}
              </v-chip>
            </td>
            <td>
              <div>{{ item.code }}</div>
            </td>
            <td>
              <div>{{ item.kind }}</div>
            </td>
            <td>
              <v-icon v-if="item.isFavorite" color="orange darken-2">mdi-star</v-icon>
              <v-icon v-else>mdi-star</v-icon>
            </td>
            <td class="no-wrap text-right">
              <div>¥ {{ item.amount | yen() }}</div>
            </td>
            <td class="no-wrap text-right">
              <div>¥ {{ item.sum | yen() }}</div>
            </td>
            <td class="no-wrap text-right">
              <v-chip v-if="item.sum != item.amount" label small color="orange" class="font-weight-bold" >¥ {{ item.sum - item.amount | yen() }}</v-chip>
            </td>
            <td>
              <v-icon small class="mr-2" @click="openEditDialog(item)">
                mdi-pencil
              </v-icon>
            </td>
            <td>
              <v-icon small class="mr-2" @click="openDeleteDialog(item)">
                mdi-delete
              </v-icon>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <v-card>
      <div>口座 ¥ {{ sumHiki | yen() }}</div>
      <span>利用 ¥ {{ sumCard | yen() }}</span>
      <div v-if="(sumHiki - sumCard) < 0" class="orange">使っていいよ額 ¥ {{ sumHiki - sumCard | yen() }}</div>
      <div v-else>使っていいよ額 ¥ {{ sumHiki - sumCard | yen() }}</div>
    </v-card>
  </div>
</template>

<script>
import axios from '@/axios/index'
import WalletEditDialog from '../components/dialog/WalletEditDialog'
import WalletDeleteDialog from '../components/dialog/WalletDeleteDialog'

export default {
  name: 'Home',
  components: {
    WalletEditDialog,
    WalletDeleteDialog
  },
  data: function () {
    return {
      sumCard: 0,
      sumHiki: 0,
      walletsOriginal: [],
      walletsFavorite: [],
      headers: [
        { text: 'Name' },
        { text: 'Code' },
        { text: 'Kind' },
        { text: 'Favorite' },
        { text: 'Amount' },
        { text: 'Sum' },
        { text: 'Diff' },
        { text: 'Edit' },
        { text: 'Delete' }
      ]
    }
  },
  methods: {
    favoriteFilter () {
      this.walletsFavorite = this.walletsOriginal
    },
    openEditDialog (item) {
      this.$refs.walletEdit.openDialog(item)
    },
    openDeleteDialog (item) {
      this.$refs.walletDelete.openDialog(item)
    },
    reload () {
      axios
        .get('/api/wallet/sum')
        .then((response) => {
          this.walletsOriginal = response.data
          this.walletsFavorite = response.data.filter((row) => {
            return (row.isFavorite === true)
          })
          const card = response.data.filter((row) => {
            return (row.kind === 'カード')
          })
          const hikiotoshi = response.data.filter((row) => {
            return (row.kind === '引き落とし')
          })
          console.log(card)
          console.log(hikiotoshi)
          this.sumCard = card.reduce((value, i) => value - i.sum, 0)
          this.sumHiki = hikiotoshi.reduce((value, i) => value + i.sum, 0)
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
    }
  },
  filters: {
    yen (value) {
      return value.toLocaleString()
    }
  },
  mounted: async function () {
    this.reload()
  }
}
</script>
