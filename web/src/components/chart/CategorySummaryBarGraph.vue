<script>
import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  data: function () {
    return {
      data: {
        // X軸の情報
        labels: [],
        // Y軸の情報
        datasets: []
      },
      options: {
        legend: {
          // 凡例
          display: true
        },
        tooltips: {
          // ツールチップ
          enabled: true
        },
        onClick: this.handleChartClick,
        scales: {
          // Y軸のオプション
          yAxes: [{
            scaleLabel: {
              fontColor: 'black'
            },
            stacked: true,
            gridLines: {
              zeroLineColor: 'black'
            },
            ticks: {
              fontColor: 'black',
              callback: function (val) {
                return '￥' + val.toLocaleString()
              }
            }
          }],
          // X軸のオプション
          xAxes: [{
            scaleLabel: {
              fontColor: 'black',
              display: true,
              labelString: '日付'
            },
            stacked: true,
            gridLines: {
              color: 'rgba(126, 126, 126, 0.4)',
              zeroLineColor: 'black'
            },
            ticks: {
              fontColor: 'black'
            }
          }]
        }
      },
      year: null,
      summary: []
    }
  },
  methods: {
    dataSet (data, year) {
      this.year = year
      this.summary = data
      this.data.labels = []
      this.data.datasets = []
      for (const i in data) {
        if (data[i].name === '振替') {
          continue
        }
        this.data.datasets.push({
          // 折れ線グラフ
          type: 'bar',
          label: data[i].name,
          data: data[i].summary,
          backgroundColor: data[i].color,
          borderColor: data[i].color,
          borderWidth: 3,
          // ポイントの背景色
          pointBackgroundColor: 'rgba(255, 99, 132, 0.2)',
          // ポイントの形(circle[○],rect[□],triangle[△]等がある)
          pointStyle: 'circle',
          // ポイントの半径
          radius: 4,
          // ホバー時のポイント背景色
          pointHoverBackgroundColor: 'rgba(255, 99, 132, 0.2)',
          // ホバー時のポイントの半径
          pointHoverRadius: 6,
          // ホバー時のポイント背景色
          pointHoverBorderColor: 'rgb(255, 99, 132)',
          // ホバー時の先の太さ
          pointHoverBorderWidth: 2,
          // ベジェ曲線の張力（0＝直線）
          lineTension: 0,
          // 線下を塗りつぶすかどうか
          fill: false
        })
      }
      for (let i = 1; i < 13; i++) {
        this.data.labels.push(`${Number(i)}月`)
      }
      this.renderChart(this.data, this.options)
    },
    handleChartClick (evt, elements) {
      var chart = this.$data._chart
      const chartIndex = chart.getElementAtEvent(evt)
      if (chartIndex.length !== 0) {
        const datasetIndex = chartIndex[0]._datasetIndex
        const position = chartIndex[0]._index
        const info = {
          datasetIndex: datasetIndex,
          valueIndex: position,
          label: chart.tooltip._data.labels[position],
          value: chart.tooltip._data.datasets[datasetIndex].data[position]
        }
        this.$router.push({
          name: 'ItemListCard',
          query: {
            category: this.summary[info.datasetIndex].pk,
            year: this.year,
            month: info.valueIndex + 1
          }
        })
      } else {
        console.log('Background clicked')
      }
    }
  }
}
</script>
