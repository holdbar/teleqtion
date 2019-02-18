<template>
  <div>
    <el-table
      v-loading="loading"
      style="width: 100%"
      :data="accounts"
      fit
      empty-text="You don't have any accounts yet."
    >
      <el-table-column
        prop="phone_number"
        label="Phone Number">
      </el-table-column>
      <el-table-column
        label="Confirmed">
        <template slot-scope="scope">
          <div v-if="scope.row.confirmed === true">
            <el-tag type="success" :hit=true>yes</el-tag>
          </div>
          <div v-else>
            <el-tag type="warning" :hit=true>no</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Active">
        <template slot-scope="scope">
          <div v-if="scope.row.active === true">
            <el-tag type="success" :hit=true>yes</el-tag>
          </div>
          <div v-else>
            <div v-if="scope.row.error_name !== null">
              <el-tooltip placement="bottom" effect="light">
                <div slot="content">
                  Error: {{scope.row.error_name}}
                  <br/>
                  Error datetime: {{scope.row.error_datetime | formatDate }}
                </div>
                <el-tag type="warning" :hit=true>no</el-tag>
              </el-tooltip>
            </div>
            <div v-else>
              <el-tag type="warning" :hit=true>no</el-tag>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Last Used">
        <template slot-scope="scope">
          <span>{{ scope.row.last_used | formatDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="Added date">
        <template slot-scope="scope">
          <span>{{ scope.row.added_at | formatDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="invites_count"
        label="Invites">
      </el-table-column>
      <el-table-column
        prop="messages_count"
        label="Messages">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Operations">
        <template slot-scope="scope">
          <div v-if="scope.row.confirmed === false">
            <el-button
              size="mini"
              type="text"
              @click="handleConfirm(scope.$index, scope.row)"
            >Confirm
            </el-button>
            <el-button
              size="mini"
              type="text"
              @click="handleDelete(scope.$index, scope.row)">
              Delete
            </el-button>
          </div>
          <div v-else>
            <el-button
              disabled
              size="mini"
              type="text"
            >Confirm
            </el-button>
            <el-button
              size="mini"
              type="text"
              @click="handleDelete(scope.$index, scope.row)">
              Delete
            </el-button>
          </div>

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
        accounts: [],
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
        HTTP.get(`telegram-accounts/?page=${page}`)
          .then(response => {
            this.accounts = response.data.results;
            this.total_pages = response.data.count;
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error getting list of accounts.',
              type: 'error'
            });
          })
          .finally(() => (this.loading = false));
      },
      deleteAccount(accountId) {
        HTTP.delete(`telegram-accounts/${accountId}`)
          .then(response => {
            if (response.status === 204) {
              this.$notify({
                title: 'Success',
                message: 'Account deleted.',
                type: 'success'
              });
              this.fetchData();
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error deleting account.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error deleting account.',
              type: 'error'
            });
          })
      },
      handleDelete(index, row) {
        this.$confirm(
          'This will permanently delete account from the system. ' +
          'Continue?',
          'Warning', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
          this.deleteAccount(row['id'])
        }).catch(() => {
        });
      },
      handleConfirm(index, row) {
        this.$root.$emit('confirmAccountShow', row['id'])
      },
    },
    mounted() {
      this.fetchData();
      this.$root.$on('newAccountAdded', (item, response) => {
        this.fetchData();
      });
      this.$root.$on('accountConfirmed', () => {
        this.fetchData();
      });
    }
  }
</script>
