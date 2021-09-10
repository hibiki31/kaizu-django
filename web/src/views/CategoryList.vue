<template>
  <div class="home">
    <CategorySubEditDialog ref="subEditDialog" />
    <CategoryBigEditDialog ref="editDialog" />
    <CategoryDeleteDialog ref="deleteDialog" />
    <CategoryMergeDialog ref="mergeDialog" />
    <v-card>
      <v-data-table
        :dense="true"
        :headers="headers"
        :expanded.sync="expanded"
        :items="bigCategory"
        :items-per-page="30"
        :footer-props="{
          'items-per-page-options': [10, 30],
          showFirstLastPage: true,
        }"
        show-expand
        multi-sort
      >
        <!-- 拡張部分 -->
        <template v-slot:expanded-item="{ item }">
          <tr :set="sub = filteredCategory(item)">
            <tr v-for="row in sub" :key="row.id">
              <td class="no-wrap">{{ row.id }}</td>
              <td>
                <router-link :to="{ path: '/', query: { categorySubId: row.id }}">
                  {{ row.name }}
                </router-link>
              </td>
              <td>{{ row.code }}</td>
              <td>
                <v-icon small class="mr-2" @click="openSubEditDialog(row)">
                  mdi-pencil
                </v-icon>
              </td>
              <td>
              <v-icon small class="mr-2" @click="openSubDeleteDialog(row)">
                mdi-delete
              </v-icon>
              </td>
              <td>
              <v-icon small class="mr-2" @click="openMergeDialog(row)">
                mdi-merge
              </v-icon>
              </td>
            </tr>
        </template>
        <!-- 行 -->
        <template v-slot:item="{ item, expand, isExpanded }" justify="right">
          <tr>
            <td>{{ item.id }}</td>
            <td>
              <v-chip label small
              :to="{ path: '/', query: { categoryBigId: item.id }}"
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
              <v-icon small class="mr-2" @click="openDialog(item)">
                mdi-pencil
              </v-icon>
            </td>
            <td>
              <v-icon small class="mr-2" @click="openBigDeleteDialog(item)">
                mdi-delete
              </v-icon>
            </td>
            <td @click="expand(!isExpanded)">
              <v-icon small class="mr-2">
                mdi-chevron-right
              </v-icon>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import CategoryBigEditDialog from '../components/dialog/CategoryBigEditDialog'
import CategorySubEditDialog from '../components/dialog/CategorySubEditDialog'
import CategoryDeleteDialog from '../components/dialog/CategoryDeleteDialog'
import CategoryMergeDialog from '../components/dialog/CategoryMergeDialog'
import axios from '@/axios/index'

export default {
  name: 'Home',
  components: {
    CategorySubEditDialog,
    CategoryBigEditDialog,
    CategoryMergeDialog,
    CategoryDeleteDialog
  },
  data: function () {
    return {
      expanded: [],
      editDialog: false,
      subEditDialog: false,
      bigCategory: [],
      subCategory: [],
      headers: [
        { text: 'Name' },
        { text: 'Code' },
        { text: 'Actions' },
        { text: 'Delete' },
        { text: 'Open' }
      ]
    }
  },
  methods: {
    filteredCategory (item) {
      var newRow = this.subCategory.filter(function (row, index) {
        if (row.categoryBigId === item.id) return true
      })
      return newRow
    },
    openDialog (item) {
      this.$refs.editDialog.openDialog(item)
    },
    openSubEditDialog (item) {
      this.$refs.subEditDialog.openDialog(item, this.bigCategory)
    },
    openBigDeleteDialog (item) {
      this.$refs.deleteDialog.openDialog(item, 'big')
    },
    openSubDeleteDialog (item) {
      this.$refs.deleteDialog.openDialog(item, 'sub')
    },
    openMergeDialog (item) {
      this.$refs.mergeDialog.openDialog(item, this.bigCategory)
    }
  },
  mounted: async function () {
    axios
      .get('/api/category/big')
      .then((response) => {
        this.bigCategory = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
    axios
      .get('/api/category/sub')
      .then((response) => {
        this.subCategory = response.data
      })
      .catch(async () => {
        this.$_pushNotice('サーバーエラーが発生しました', 'error')
      })
  }
}
</script>
