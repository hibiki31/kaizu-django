<template>
<div class="summary">
    <v-container>
        <v-row>
            <v-col cols="12" md="6">
                <v-card class="ma-5 pa-3">
                    <v-text-field
                    spellcheck="false"
                    label="日付"
                    type="date"
                    placeholder=" "
                    v-model="selectDate"
                    ></v-text-field>
                    <v-btn icon
                    v-on:click="this.clickButton"
                    >
                    <v-icon>mdi-magnify</v-icon>
                    </v-btn>
                </v-card>
                <v-card class="ma-5">
                    <CategorySummary ref='categorySummary' />
                </v-card>
            </v-col>
            <v-col cols="12" md="6">
                <v-card class="ma-5 pa-3">
                  <v-data-table
                    dense
                    :items-per-page="30"
                    :headers="headers"
                    :items="this.summary"
                  >
                  <template v-slot:[`item.categoryBigName`]="{ item }">
                    <v-chip label small
                      :to="{ path: '/', query: { categoryBigId: item.categoryBigId , startDate: startDate, endDate: endDate }}"
                      v-bind:class="[ 'font-weight-bold', 'no-wrap', 'px-1', ]"
                      v-bind:style="{ background: item.categoryBigColor }"
                    >
                      {{ item.categoryBigName }}
                    </v-chip>
                  </template>
                  <template v-slot:[`item.sum`]="{ item }">
                    ¥ {{ item.sum | yen() }}
                  </template>
                  </v-data-table>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</div>
</template>

<script>
import axios from '@/axios/index'
import CategorySummary from '../components/chart/CategorySummaryChart'

export default {
  name: 'Home',
  data: function () {
    return {
      selectDate: '',
      startDate: '',
      endDate: '',
      summary: [],
      headers: [
        { text: 'NAME', value: 'categoryBigName' },
        { text: 'SUM', value: 'sum' }
      ],
      data: {
        datasets: [{
          data: [],
          backgroundColor: []
        }],
        labels: [
        ]
      }
    }
  },
  components: {
    CategorySummary
  },
  filters: {
    yen (value) {
      return value.toLocaleString()
    }
  },
  methods: {
    clickButton () {
      this.monthQuery(this.selectDate)
    },
    monthQuery (dateStr) {
      var date = new Date()
      if (dateStr) {
        date = new Date(dateStr)
      }
      var firstDate = new Date(date.getFullYear(), date.getMonth(), 1)
      var lastDate = new Date(date.getFullYear(), date.getMonth() + 1, 0)

      var start = (firstDate.getFullYear() + '-' + (firstDate.getMonth() + 1) + '-' + firstDate.getDate())
      var end = (lastDate.getFullYear() + '-' + (lastDate.getMonth() + 1) + '-' + lastDate.getDate())

      this.startDate = start
      this.endDate = end

      this.getSummary(start, end)
    },
    setSummary () {
      this.$refs.categorySummary.dataSet(this.data)
    },
    getSummary (startDate, endDate) {
      Object.assign(this.$data.data, this.$options.data().data)
      axios
        .get('/api/category/summary', { params: { year: '2021', month: '01' } })
        .then((response) => {
          for (const i in response.data) {
            this.data.datasets[0].data.unshift(response.data[i].sum)
            this.data.labels.unshift(response.data[i].categoryBigName)
            this.data.datasets[0].backgroundColor.unshift(response.data[i].categoryBigColor)
          }
          this.summary = response.data
          this.setSummary()
        })
        .catch(async () => {
          this.$_pushNotice('サーバーエラーが発生しました', 'error')
        })
    }
  },
  mounted: async function () {
    this.monthQuery()
  }
}
</script>
