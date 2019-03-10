<template>
  <div>
    <h1>My Dashboard</h1>

    <div id="charts" v-if="messages.total || invites.total">
      <div>
        <b>Total</b>
        <chart-total :messages=messages.total
                     :invites=invites.total
                     :width=250 :height=250>
        </chart-total>
      </div>
      <div>
        <b>Invites</b>
        <chart-results :success_count=invites.success
                       :error_count=invites.error
                       :width=250 :height=250>
        </chart-results>
      </div>
      <div>
        <b>Messages</b>
        <chart-results :success_count=messages.success
                       :error_count=messages.error
                       :width=250 :height=250>
        </chart-results>
      </div>
    </div>

    <tutorial-accordion/>
  </div>
</template>


<script>
  import {HTTP} from '../http-common'
  import TutorialAccordion from './TutorialAccordion'
  import ChartTotal from './ChartTotal'
  import ChartResults from './ChartResults'

  export default {
    components: {
      TutorialAccordion, ChartTotal, ChartResults
    },
    data() {
      return {
        messages: {
          total: 0,
          success: 0,
          error: 0
        },
        invites: {
          total: 0,
          success: 0,
          error: 0
        },
      };
    },
    methods: {
      fetchData() {
        HTTP.get(`actions/statistics/`)
          .then(response => {
            this.messages = response.data.messages;
            this.invites = response.data.invites;
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error getting statistics.',
              type: 'error'
            });
          });
      },
    },
    mounted() {
      this.fetchData();
    }
  }
</script>

<style scoped>
  #charts {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
  }

  #charts > div {
    width: 300px;
    height: 300px;
  }
</style>
