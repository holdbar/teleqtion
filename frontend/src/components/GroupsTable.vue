<template>
  <div>
    <el-table
      v-loading="loading"
      style="width: 100%"
      :data="groups"
      tooltip-effect="light"
      fit
      empty-text="You don't have any groups yet."
    >
      <el-table-column
        prop="title"
        label="Title"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="username"
        label="Username"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="join_link"
        label="Join Link"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="scrapped_count"
        label="Scrapped">
      </el-table-column>
      <el-table-column
        prop="invited_to_count"
        label="Invited To">
      </el-table-column>
      <el-table-column
        prop="invited_from_count"
        label="Invited From">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Operations">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">Delete
          </el-button>
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
        groups: [],
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
        HTTP.get(`entities/groups/?page=${page}`)
          .then(response => {
            this.groups = response.data.results;
            this.total_pages = response.data.count;
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error getting list of groups.',
              type: 'error'
            });
          })
          .finally(() => (this.loading = false));
      },
      deleteGroup(groupId) {
        HTTP.delete(`entities/groups/${groupId}`)
          .then(response => {
            if (response.status === 204) {
              this.$notify({
                title: 'Success',
                message: 'Group deleted.',
                type: 'success'
              });
              this.fetchData();
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error deleting group.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.errors.push(e);
            this.$notify({
              title: 'Error',
              message: 'Error deleting group.',
              type: 'error'
            });
          })
      },
      handleDelete(index, row) {
        this.$confirm(
          'This will permanently delete group and ' +
          'all scrapped users. Continue?',
          'Warning', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
          this.deleteGroup(row['id'])
        }).catch(() => {
        });
      },
    },
    mounted() {
      this.fetchData();
      this.$root.$on('newGroupAdded', (item, response) => {
        this.fetchData();
      });
    }
  }
</script>
