<script>
  import {Pie} from 'vue-chartjs'

  export default {
    extends: Pie,
    props: ['success_count', 'error_count'],
    mounted() {
      this.renderChart({
          labels: ['Successful', 'Errors',],
          datasets: [
            {
              backgroundColor: [
                '#00760d',
                '#a70900',
              ],
              data: [this.success_count, this.error_count]
            }
          ]
        },
        {responsive: true, maintainAspectRatio: false})
    }
  }
</script>
