<template>
  <div class="summary">
    <v-container>
      <v-card class="ma-5 pa-3">
        <v-text-field
          spellcheck="false"
          label="日付"
          type="month"
          placeholder=" "
          v-model="selectDate"
          @change="getSummary(selectDate)"
        ></v-text-field>
      </v-card>
      <v-row>
        <v-col cols="12" md="12">
          <v-card class="ma-5">
            <CategorySummaryBarGraph
              ref="categorySummaryBarGraph"
              :height="230"
            />
          </v-card>
        </v-col>
        <v-col cols="12" md="12">
          <v-card class="ma-5">
            <CategorySummaryGraph ref="categoryGraph" :height="230" />
          </v-card>
        </v-col>
        <v-col cols="12" md="12">
          <v-card class="ma-5 pa-3">
            <v-data-table
              dense
              :items-per-page="30"
              :headers="headers"
              :items="this.summary"
            >
              <template v-slot:item="{ item }" justify="right">
                <tr>
                  <td>
                    <v-chip
                      label
                      small
                      :to="{
                        path: '/item/',
                        query: {
                          category: item.pk,
                          year: selectDate.split('-')[0],
                          month: selectDate.split('-')[1],
                        },
                      }"
                      v-bind:class="['font-weight-bold', 'no-wrap', 'px-1']"
                      v-bind:style="{ background: item.color }"
                    >
                      {{ item.name }}
                    </v-chip>
                  </td>
                  <td
                    v-for="(sum, index) in item.summary"
                    :key="index"
                    class="no-wrap text-right"
                  >
                    ¥ {{ sum | yen }}
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card class="ma-5 pa-3">
            <v-text-field
              spellcheck="false"
              label="日付"
              type="month"
              placeholder=" "
              v-model="selectDate"
            ></v-text-field>
            <v-btn icon v-on:click="this.clickButton">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-card>
          <v-card class="ma-5">
            <CategorySummaryChart ref="categorySummary" />
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from '@/axios/index'
import CategorySummaryChart from '../components/chart/CategorySummaryChart'
import CategorySummaryGraph from '../components/chart/CategorySummaryMonthGraph'
import CategorySummaryBarGraph from '../components/chart/CategorySummaryBarGraph'

export default {
  name: 'Home',
  data: function () {
    return {
      selectDate: '',
      startDate: '',
      endDate: '',
      summary: [],
      headers: [
        { text: 'NAME', value: 'name' },
        { text: '1月', value: 'month_1' },
        { text: '2月', value: 'month_2' },
        { text: '3月', value: 'month_3' },
        { text: '4月', value: 'month_4' },
        { text: '5月', value: 'month_5' },
        { text: '6月', value: 'month_6' },
        { text: '7月', value: 'month_7' },
        { text: '8月', value: 'month_8' },
        { text: '9月', value: 'month_9' },
        { text: '10月', value: 'month_10' },
        { text: '11月', value: 'month_11' },
        { text: '12月', value: 'month_12' }
      ],
      data: {
        datasets: [
          {
            data: [],
            backgroundColor: []
          }
        ],
        labels: []
      }
    }
  },
  components: {
    CategorySummaryChart,
    CategorySummaryGraph,
    CategorySummaryBarGraph
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
      this.getSummary(dateStr)
    },
    setSummary () {
      this.$refs.categorySummary.dataSet(this.data)
      this.$refs.categoryGraph.dataSet(this.summary)
      this.$refs.categorySummaryBarGraph.dataSet(
        this.summary,
        this.selectDate.split('-')[0]
      )
    },
    getSummary (dateStr) {
      axios
        .get('/api/category/summary', {
          params: { year: dateStr.split('-')[0], month: dateStr.split('-')[1] }
        })
        .then((response) => {
          this.data.datasets[0].data = []
          this.data.labels = []
          this.data.datasets[0].backgroundColor = []
          for (const i in response.data) {
            if (
              response.data[i].name !== '振替' &&
              response.data[i].summary !== 0
            ) {
              this.data.datasets[0].data.unshift(response.data[i].summary)
              this.data.labels.unshift(response.data[i].name)
              this.data.datasets[0].backgroundColor.unshift(
                response.data[i].color
              )
            }
          }
          this.summary = response.data
          this.setSummary()
        })
    }
  },
  mounted: async function () {
    var toDay = new Date()
    this.selectDate = `${toDay.getFullYear()}-${(
      '0' +
      (toDay.getMonth() + 1)
    ).slice(-2)}`
    console.log(this.selectDate)
    this.getSummary(this.selectDate)
  }
}
</script>
