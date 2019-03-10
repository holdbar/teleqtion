<script>
  import {Pie} from 'vue-chartjs'

  export default {
    extends: Pie,
    props: ['messages', 'invites'],
    mounted() {
      this.renderChart({
          labels: ['Messages', 'Invites',],
          datasets: [
            {
              backgroundColor: [
                '#5f4bb8',
                '#008eff',
              ],
              data: [this.messages, this.invites]
            }
          ]
        },
        {responsive: true, maintainAspectRatio: false})
    }
  }
</script>
