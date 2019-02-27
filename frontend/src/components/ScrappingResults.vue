<template>
  <el-row>
    <el-col :sm="24" :md="10">
      <div class="sub-title">Select group</div>
      <el-autocomplete
        v-model="searchGroup"
        :fetch-suggestions="fetchGroups"
        value-key="title"
        clearable
        placeholder="Group name or username"
        @select="handleSelectGroup"
        @clear="handleClearInput"
      ></el-autocomplete>
      <h3 v-if="this.totalContacts > 10">
        Total scrapped users:
        <el-tag :hit=true>{{ this.totalContacts }}</el-tag>
      </h3>
    </el-col>
    <el-col :sm="24" :md="14">
      <el-button v-show="this.fetchedContacts.length"
                 type="danger"
                 plain
                 @click="handleDeleteContactsAll">
        Remove all <i class="el-icon-delete"></i>
      </el-button>
      <transition name="el-fade-in-linear">
        <el-button v-show="this.selectedContacts.length"
                   type="warning"
                   plain
                   @click="handleDeleteContactsSelected">
          Remove selected
        </el-button>
      </transition>
      <el-table
        v-loading="loading"
        style="width: 100%"
        :data="fetchedContacts"
        fit
        empty-text="This group does not have any scrapped users yet."
        @selection-change="handleSelectContacts">
        <el-table-column
          type="selection"
          width="55">
        </el-table-column>
        <el-table-column label="Username">
          <template slot-scope="scope">
            <a :href="generateTelegramLink(scope.row.username)"
               class="scrappedUserLink"
               target="_blank">
              {{ scope.row.username }}
            </a>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="this.totalContacts > 10"
                     layout="prev, pager, next"
                     @current-change="handleCurrentPageChange"
                     :total=this.totalContacts>
      </el-pagination>
    </el-col>
  </el-row>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      return {
        searchGroup: '',
        selectedGroup: null,
        selectedContacts: [],
        fetchedGroups: [],
        fetchedContacts: [],
        totalContacts: 1,
        loading: false,
      }
    },
    methods: {
      fetchGroups(queryString, cb) {
        HTTP.get(`entities/groups/?search=${queryString}`)
          .then(response => {
            if (response.status === 200) {
              this.fetchedGroups = response.data.results;
              cb(this.fetchedGroups);
            } else {
              this.$message({
                message: 'Error getting list of groups.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$message({
            message: 'Error getting list of groups.',
            type: 'error'
          });
        })
      },
      generateTelegramLink(username) {
        return `https://t.me/${username}`;
      },
      handleSelectContacts(val) {
        this.selectedContacts = val;
      },
      handleSelectGroup(item) {
        this.selectedGroup = item;
        this.fetchContacts();
      },
      handleClearInput() {
        this.selectedGroup = null;
        this.totalContacts = 0;
        this.fetchedContacts = [];
      },
      handleCurrentPageChange(val) {
        this.fetchContacts(val);
      },
      fetchContacts(page) {
        this.loading = true;
        if (page === undefined) {
          page = 1;
        }
        HTTP.get(`entities/contacts/?group=${this.selectedGroup.id}&page=${page}`)
          .then(response => {
            if (response.status === 200) {
              this.fetchedContacts = response.data.results;
              this.totalContacts = response.data.count;
            } else {
              this.$message({
                message: 'Error getting list of scrapped contacts.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$message({
            message: 'Error getting list of scrapped contacts.',
            type: 'error'
          });
        });
        this.loading = false;
      },
      deleteContact(contactId) {
        HTTP.delete(`entities/contacts/${contactId}/`)
          .then(response => {
            if (response.status === 204) {
              this.$message({
                message: `Contact successfully deleted.`,
                type: 'success'
              });
            } else {
              this.$message({
                message: `Error deleting contact.`,
                type: 'error'
              });
            }
          }).catch(e => {
          this.$message({
            message: `Error deleting contact.`,
            type: 'error'
          });
        });
      },
      deleteContactList(idsList) {
        return HTTP.post(`entities/contacts/delete-list/`, {
          id_list: idsList
        }).then(response => {
          if (response.status === 200) {
            this.$message({
              message: `${idsList.length} contacts successfully deleted.`,
              type: 'success'
            });
            this.$emit('refetchNeeded');
          } else {
            this.$message({
              message: `Error deleting contacts.`,
              type: 'error'
            });
          }
        }).catch(e => {
          this.$message({
            message: `Error deleting contacts.`,
            type: 'error'
          });
        });
      },
      deleteContactsByGroup(groupId) {
        return HTTP.post(`entities/contacts/delete-all/`, {
          group_id: groupId
        }).then(response => {
          if (response.status === 200) {
            this.$message({
              message: `All contacts successfully deleted.`,
              type: 'success'
            });
            this.$emit('refetchNeeded');
          } else {
            this.$message({
              message: `Error deleting contacts.`,
              type: 'error'
            });
          }
        }).catch(e => {
          this.$message({
            message: `Error deleting contacts.`,
            type: 'error'
          });
        });
      },
      handleDeleteContactsAll() {
        this.$confirm(
          `This will permanently delete all ${this.totalContacts} scrapped
           users from selected group. Anyway, you'll be able to
           scrape them again. Continue?`,
          'Warning', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
          this.loading = true;
          this.deleteContactsByGroup(this.selectedGroup.id);
        }).catch(() => {
        });
      },
      handleDeleteContactsSelected() {
        this.$confirm(
          `This will permanently delete all
          ${this.selectedContacts.length} selected users. Continue?`,
          'Warning', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
          this.loading = true;
          let contactsIds = this.selectedContacts.map(i => i.id);
          this.deleteContactList(contactsIds);
        }).catch(() => {
        });
      },
    },
    mounted() {
      this.$on('refetchNeeded', () => {
        this.handleSelectGroup(this.selectedGroup);
      });
    }
  }
</script>

<style scoped>
  .sub-title {
    margin: 15px 0;
  }

  .el-autocomplete {
    width: 70%;
  }

  button {
    float: left;
  }

  .scrappedUserLink {
    text-decoration: none;
    color: #409EFF;
    font-weight: 500;
  }
</style>
