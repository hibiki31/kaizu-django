<script>
import { Doughnut } from 'vue-chartjs'

export default {
  extends: Doughnut,
  data: function () {
    return {
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
  methods: {
    dataSet (data) {
      this.data = data
      this.renderChart(this.data, this.options)
    }
  }
}
</script>
