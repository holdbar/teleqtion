<template>
  <div>
    <el-table
      v-loading="loading"
      style="width: 100%"
      :data="transactions"
      fit
      empty-text="You didn't make any payments yet.">
      <el-table-column
        prop="currency"
        label="Currency">
      </el-table-column>
      <el-table-column
        prop="amount_original"
        label="Amount">
      </el-table-column>
      <el-table-column
        prop="amount_paid"
        label="Amount Paid">
      </el-table-column>
      <el-table-column
        prop="amount"
        label="Amount (USD)">
      </el-table-column>
      <el-table-column
        label="Status">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.status === 'PAID'" type="success">SUCCESS</el-tag>
          <el-tag v-else-if="scope.row.status === 'PEND'" type="info">PENDING</el-tag>
          <el-tag v-else-if="scope.row.status === 'TOUT'" type="danger">TIMED OUT</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="Datetime">
        <template slot-scope="scope">
          {{scope.row.created_at | formatDate }}
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-if="this.total_pages > 10"
                   layout="prev, pager, next"
                   @current-change="handleCurrentPageChange"
                   :total=this.total_pages>
    </el-pagination>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      return {
        transactions: [],
        total_pages: 1,
        loading: true,
      }
    },
    methods: {
      handleCurrentPageChange(val) {
        this.fetchData(val);
      },
      fetchData(page) {
        this.loading = true;
        if (page === undefined) {
          page = 1;
        }
        HTTP.get(`payments/crypto/?page=${page}`)
          .then(response => {
            this.transactions = response.data.results;
            this.total_pages = response.data.count;
          }).catch(e => {
          this.$notify({
            title: 'Error',
            message: 'Error getting list of transactions.',
            type: 'error'
          });
        }).finally(() => (this.loading = false));
      },
    },
    mounted() {
      this.fetchData();
      this.$root.$on('updateTransactionsTable', () => {
        this.fetchData();
      });
    }
  }
</script>
