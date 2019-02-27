<template>
  <div v-loading="loading" element-loading-text="Please, wait. Scrapping in progress.">
    <p style="text-align: start; margin: 3% 0">
      Here you can scrape your groups. System will automatically
      sort scrapped users by their last online time, skip admins and bots.
    </p>
    <el-form ref="scrapeForm"
             :model="scrapeForm"
             :rules="rules"
             :hide-required-asterisk=true
             label-width="150px"
             @submit.prevent.native="onSubmit">
      <el-form-item label="Group" prop="selectedGroup">
        <el-autocomplete
          v-model="searchGroup"
          :fetch-suggestions="fetchGroups"
          value-key="title"
          clearable
          placeholder="Group name or username"
          @select="handleSelectGroup"
          @clear="handleClearGroup"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="Use my account">
        <el-switch v-if="this.fetchedAccounts.length"
                   v-model="scrapeForm.useCustomAccount">
        </el-switch>
        <el-tooltip v-else effect="dark" content="You have no active accounts." placement="bottom">
          <el-switch v-model="scrapeForm.useCustomAccount" disabled></el-switch>
        </el-tooltip>
      </el-form-item>
      <transition name="el-zoom-in-center">
        <el-form-item label="Account" prop="customAccount" v-show="scrapeForm.useCustomAccount">
          <el-autocomplete
            v-model="searchAccount"
            :fetch-suggestions="fetchAccounts"
            value-key="phone_number"
            clearable
            placeholder="Phone number"
            prefix-icon="el-icon-mobile-phone"
            @select="handleSelectAccount"
            @clear="handleClearAccount"
          ></el-autocomplete>
        </el-form-item>
      </transition>
      <el-form-item>
        <el-button type="primary" round @click="onSubmit">
          Scrape <i class="el-icon-d-arrow-right el-icon-right"></i>
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validateGroup = (rule, value, callback) => {
        if (!this.scrapeForm.selectedGroup) {
          callback(new Error('Please select one of your groups'));
        }
        callback();

      };
      let validateCustomAccount = (rule, value, callback) => {
        if (this.scrapeForm.useCustomAccount && !this.scrapeForm.customAccount) {
          callback(new Error('Please select one of your accounts'));
        }
        callback();
      };
      return {
        loading: false,
        taskId: null,
        intervalCheck: null,
        searchGroup: '',
        searchAccount: '',
        scrapeForm: {
          selectedGroup: '',
          useCustomAccount: false,
          customAccount: ''
        },
        fetchedGroups: [],
        fetchedAccounts: [],
        rules: {
          selectedGroup: [
            {validator: validateGroup, type: 'object', trigger: 'change'},
          ],
          customAccount: [
            {validator: validateCustomAccount, trigger: 'change'}
          ],
        }
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
      fetchAccounts(queryString, cb) {
        // HTTP.get(`telegram-accounts/?phone_number=${queryString}&active=t`)
        HTTP.get(`telegram-accounts/?phone_number=${queryString}`)
          .then(response => {
            if (response.status === 200) {
              this.fetchedAccounts = response.data.results;
              cb(this.fetchedAccounts);
            } else {
              this.$message({
                message: 'Error getting list of accounts.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$message({
            message: 'Error getting list of accounts.',
            type: 'error'
          });
        })
      },
      handleSelectAccount(item) {
        this.scrapeForm.customAccount = item;
      },
      handleSelectGroup(item) {
        this.scrapeForm.selectedGroup = item;
      },
      startScrapping() {
        this.loading = true;
        if (this.scrapeForm.useCustomAccount) {
          var post_data = {
            group_id: this.scrapeForm.selectedGroup.id,
            telegram_account_id: this.scrapeForm.customAccount.id,
          };
        } else {
          var post_data = {
            group_id: this.scrapeForm.selectedGroup.id,
          };
        }
        HTTP.post('actions/scrapping/start', post_data)
          .then(response => {
            if (response.status === 200) {
              this.taskId = response.data['task_id'];
              this.intervalCheck = setInterval(function () {
                this.checkTaskStatus(true);
              }.bind(this), 1000);
            } else {
              this.$message({
                message: 'Failed to launch scrapping.',
                type: 'error'
              });
              this.loading = false;
            }
          }).catch(e => {
          this.$message({
            message: 'Failed to launch scrapping.',
            type: 'error'
          });
          this.loading = false;
        })
      },
      checkTaskStatus() {
        HTTP.get(`task-status/${this.taskId}/`)
          .then(response => {
              if ('success' in response.data) {
                if (response.data['success'] === true) {
                  this.$message({
                    message: 'Scrapping finished!',
                    type: 'success'
                  });
                  this.loading = false;
                } else {
                  this.$message({
                    message: response.data['error'],
                    type: 'error'
                  });
                  this.loading = false;
                }
                clearInterval(this.intervalCheck);
                this.loading = false;
                this.intervalCheck = null;
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error checking scrapping status.',
            type: 'error'
          });
        });
      },
      onSubmit() {
        this.$refs['scrapeForm'].validate((valid) => {
          if (valid) {
            this.startScrapping();
          } else {
            return false;
          }
        });
      },
      handleClearGroup() {
        this.scrapeForm.selectedGroup = null;
      },
      handleClearAccount() {
        this.scrapeForm.customAccount = null;
      }
    },
    mounted() {
      this.fetchAccounts('', function () {
      });
    }
  }
</script>

<style scoped>
  .el-autocomplete {
    min-width: 50%;
  }
  .el-form-item__error {
    position: relative;
  }
</style>
