<template>
  <div v-loading="loading" element-loading-text="Please, wait. Inviting in progress.">
    <el-steps :active="4" align-center>
      <el-step title="Select source group" icon="el-icon-upload2"></el-step>
      <el-step title="Select target group" icon="el-icon-download"></el-step>
      <el-step title="Set amount of users to invite" icon="el-icon-question"></el-step>
      <el-step title="Start inviting!" icon="el-icon-check"></el-step>
    </el-steps>
    <el-form :model="invitingForm"
             :hide-required-asterisk=true
             :rules="rules"
             ref="invitingForm"
             label-width="15em"
             @submit.prevent.native="onSubmit">
      <el-form-item label="Source Group" prop="sourceGroup">
        <el-autocomplete
          v-model="searchSourceGroup"
          :fetch-suggestions="fetchGroups"
          value-key="title"
          clearable
          prefix-icon="el-icon-upload2"
          placeholder="Source group name or username"
          @select="handleSelectSourceGroup"
          @clear="handleClearSourceGroup"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="Target Group" prop="targetGroup">
        <el-autocomplete
          v-model="searchTargetGroup"
          :fetch-suggestions="fetchGroups"
          value-key="title"
          clearable
          prefix-icon="el-icon-download"
          placeholder="Target group name or username"
          @select="handleSelectTargetGroup"
          @clear="handleClearTargetGroup"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="Amount of users to invite" prop="amount">
        <el-slider
          v-model="invitingForm.amount"
          show-input
          :min=0
          :max=maxInvitesAmount
          class="amountSlider">
        </el-slider>
        <div v-show="invitingForm.amount > 0">
          About {{ approximatePrice() }} $ will be withdrawn from your balance.
        </div>
      </el-form-item>
      <el-form-item label="Use system accounts" prop="useSystemNumbers">
        <el-switch v-if="this.userHasOwnAccounts"
                   v-model="invitingForm.useSystemNumbers">
        </el-switch>
        <el-tooltip v-else
                    effect="dark"
                    content="You have no active accounts,
                             so only system accounts can be used."
                    placement="bottom">
          <el-switch v-model="invitingForm.useSystemNumbers" disabled></el-switch>
        </el-tooltip>
      </el-form-item>
      <el-form-item>
        <el-button v-if="this.maxInvitesAmount > 0" type="primary" @click="onSubmit">Start inviting</el-button>
        <el-button v-else type="primary" disabled>Start inviting</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validateSourceGroup = (rule, value, callback) => {
        if (!this.invitingForm.sourceGroup) {
          callback(new Error('Please select group to invite users from.'));
        } else if (
          this.invitingForm.sourceGroup && this.invitingForm.targetGroup &&
          this.invitingForm.sourceGroup.id === this.invitingForm.targetGroup.id
        ) {
          callback(new Error('Source and Target group can\'t be same.'));
        }
        callback();
      };
      let validateTargetGroup = (rule, value, callback) => {
        if (!this.invitingForm.targetGroup) {
          callback(new Error('Please select group to invite users to.'));
        } else if (
          this.invitingForm.sourceGroup && this.invitingForm.targetGroup &&
          this.invitingForm.sourceGroup.id === this.invitingForm.targetGroup.id
        ) {
          callback(new Error('Source and Target group can\'t be same.'));
        }
        callback();
      };
      return {
        loading: false,
        userHasOwnAccounts: false,
        fetchedGroups: [],
        searchSourceGroup: '',
        searchTargetGroup: '',
        maxInvitesAmount: 500,
        taskId: null,
        intervalCheck: null,
        invitingForm: {
          sourceGroup: '',
          targetGroup: '',
          amount: 0,
          useSystemNumbers: true
        },
        rules: {
          sourceGroup: [
            {validator: validateSourceGroup, type: 'object', trigger: 'change'},
          ],
          targetGroup: [
            {validator: validateTargetGroup, type: 'object', trigger: 'change'}
          ],
        }
      }
    },
    methods: {
      onSubmit() {
        this.$refs['invitingForm'].validate((valid) => {
          if (valid) {
            this.startInviting();
            this.handleClearTargetGroup();
            this.handleClearSourceGroup();
          } else {
            return false;
          }
        });
      },
      resetFields() {
        this.searchSourceGroup = '';
        this.searchTargetGroup = '';
        this.invitingForm.amount = 0;
      },
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
      handleSelectSourceGroup(item) {
        this.invitingForm.sourceGroup = item;
        this.fetchMaxInvitesAmount();
      },
      handleSelectTargetGroup(item) {
        this.invitingForm.targetGroup = item;
      },
      checkTaskStatus() {
        HTTP.get(`task-status/${this.taskId}/`)
          .then(response => {
              if ('success' in response.data) {
                if (response.data['success'] === true) {
                  this.$message({
                    message: 'Inviting finished!',
                    type: 'success'
                  });
                  this.loading = false;
                  this.handleClearTargetGroup();
                  this.handleClearSourceGroup();
                  this.resetFields();
                  this.$root.$emit('fetchBalance');
                } else {
                  this.$message({
                    message: response.data['error'],
                    type: 'error'
                  });
                  this.loading = false;
                  this.handleClearTargetGroup();
                  this.handleClearSourceGroup();
                  this.resetFields();
                  this.$root.$emit('fetchBalance');
                }
                clearInterval(this.intervalCheck);
                this.loading = false;
                this.intervalCheck = null;
                this.handleClearTargetGroup();
                this.handleClearSourceGroup();
                this.resetFields();
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error checking inviting status.',
            type: 'error'
          });
        });
      },
      handleClearSourceGroup() {
        this.invitingForm.sourceGroup = null;
        this.maxInvitesAmount = 0;
      },
      handleClearTargetGroup() {
        this.invitingForm.targetGroup = null;
        this.maxInvitesAmount = 0;
      },
      fetchMaxInvitesAmount() {
        if (this.invitingForm.sourceGroup) {
          this.fetchMaxInvitesFromSourceGroup();
        } else if (this.invitingForm.sourceGroup && this.invitingForm.targetGroup) {
          this.fetchMaxInvitesFromBothGroups();
        }
      },
      fetchMaxInvitesFromSourceGroup() {
        HTTP.get(`entities/contacts/?group=${this.invitingForm.sourceGroup.id}`)
          .then(response => {
              if (response.status === 200) {
                if (response.data.count === 0) {
                  this.maxInvitesAmount = 0;
                  this.$notify({
                    title: 'Oops!',
                    message: 'Source Group does not have scrapped users yet.',
                    type: 'warning'
                  });
                } else if (response.data.count <= 500) {
                  this.maxInvitesAmount = response.data.count;
                } else {
                  this.maxInvitesAmount = 500;
                }
              } else {
                this.$message({
                  message: 'Error getting number of scrapped users.',
                  type: 'error'
                });
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error getting number of scrapped users.',
            type: 'error'
          });
        });
      },
      fetchMaxInvitesFromBothGroups() {
        HTTP.post(`entities/contacts/get-not-invited-count/`, {
          source_group_id: this.invitingForm.sourceGroup.id,
          target_group_id: this.invitingForm.targetGroup.id
        }).then(response => {
            if (response.status === 200) {
              if (response.data.count === 0) {
                this.maxInvitesAmount = 0;
                this.$notify({
                  title: 'Oops!',
                  message: `It seems like all users
                            from source group have been
                            already invited to the target group.`,
                  type: 'warning'
                });
              } else if (response.data.count <= 500) {
                this.maxInvitesAmount = response.data.count;
              } else {
                this.maxInvitesAmount = 500;
              }
            } else {
              this.$message({
                message: 'Error getting number of scrapped users.',
                type: 'error'
              });
            }
          }
        ).catch(e => {
          this.$message({
            message: 'Error getting number of scrapped users.',
            type: 'error'
          });
        });
      },
      checkIfUserHasOwnAccounts() {
        HTTP.get(`telegram-accounts/?active=t`)
          .then(response => {
              if (response.status === 200) {
                this.userHasOwnAccounts = response.data.count > 0;
              } else {
                this.$message({
                  message: 'Error getting list of active accounts.',
                  type: 'error'
                });
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error getting list of active accounts.',
            type: 'error'
          });
        });
      },
      startInviting() {
        this.loading = true;

        HTTP.post('actions/inviting/start', {
          source_group_id: this.invitingForm.sourceGroup.id,
          target_group_id: this.invitingForm.targetGroup.id,
          use_system_numbers: this.invitingForm.useSystemNumbers,
          limit: this.invitingForm.amount
        }).then(response => {
          if (response.status === 200) {
            this.taskId = response.data['task_id'];
            this.intervalCheck = setInterval(function () {
              this.checkTaskStatus(true);
            }.bind(this), 1000);
          } else {
            this.$message({
              message: 'Failed to launch inviting.',
              type: 'error'
            });
            this.loading = false;
          }
        }).catch(e => {
          this.$message({
            message: 'Failed to launch inviting.',
            type: 'error'
          });
          this.loading = false;
        })
      },
       approximatePrice() {
        let price = this.invitingForm.useSystemNumbers ? 0.06 : 0.04;
        let result = this.invitingForm.amount * price;
        return result.toFixed(2);
      },
    },
    mounted() {
      this.checkIfUserHasOwnAccounts();
    }
  }
</script>

<style scoped>
  .el-form {
    margin: 5% 0;
  }

  .el-autocomplete {
    min-width: 50em;
  }

  .amountSlider {
    max-width: 50em;
    padding-left: 8.5em;
  }
</style>
