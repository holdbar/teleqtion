<template>
  <div v-loading="loading" element-loading-text="Please, wait. Messaging in progress.">
    <el-steps :active="4" align-center>
      <el-step title="Select group" icon="el-icon-upload2"></el-step>
      <el-step title="Select message" icon="el-icon-message"></el-step>
      <el-step title="Set amount of users to send message to" icon="el-icon-question"></el-step>
      <el-step title="Start messaging!" icon="el-icon-check"></el-step>
    </el-steps>
    <el-form :model="messagingForm"
             :hide-required-asterisk=true
             :rules="rules"
             ref="messagingForm"
             label-width="15em"
             @submit.prevent.native="onSubmit">
      <el-form-item label="Group" prop="Group">
        <el-autocomplete
          v-model="searchGroup"
          :fetch-suggestions="fetchGroups"
          value-key="title"
          clearable
          prefix-icon="el-icon-upload2"
          placeholder="Group name or username"
          @select="handleSelectGroup"
          @clear="handleClearGroup"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="Message" prop="message">
        <el-autocomplete
          v-model="searchMessage"
          :fetch-suggestions="fetchMessages"
          value-key="title"
          clearable
          prefix-icon="el-icon-message"
          placeholder="Your message title"
          @select="handleSelectMessage"
          @clear="handleClearMessage"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="Amount of users to send message to" prop="amount">
        <el-slider
          v-model="messagingForm.amount"
          show-input
          :min=0
          :max=maxMessagesAmount
          class="amountSlider">
        </el-slider>
        <div v-show="messagingForm.amount > 0">
          About {{ approximatePrice() }} $ will be withdrawn from your balance.
        </div>
      </el-form-item>
      <el-form-item label="Use system accounts" prop="useSystemNumbers">
        <el-switch v-if="this.userHasOwnAccounts"
                   v-model="messagingForm.useSystemNumbers">
        </el-switch>
        <el-tooltip v-else
                    effect="dark"
                    content="You have no active accounts,
                             so only system accounts can be used."
                    placement="bottom">
          <el-switch v-model="messagingForm.useSystemNumbers" disabled></el-switch>
        </el-tooltip>
      </el-form-item>
      <el-form-item>
        <el-button v-if="maxMessagesAmount > 0" type="primary" @click="onSubmit">Start messaging</el-button>
        <el-button v-else type="primary" disabled>Start messaging</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validateGroup = (rule, value, callback) => {
        if (!this.messagingForm.group) {
          callback(new Error('Please select group to message users from.'));
        }
        callback();
      };
      let validateMessage = (rule, value, callback) => {
        if (!this.messagingForm.message) {
          callback(new Error('Please select message.'));
        }
        callback();
      };
      return {
        loading: false,
        userHasOwnAccounts: false,
        fetchedGroups: [],
        fetchedMessages: [],
        searchGroup: '',
        searchMessage: '',
        maxMessagesAmount: 500,
        taskId: null,
        intervalCheck: null,
        messagingForm: {
          group: '',
          message: '',
          amount: 1,
          useSystemNumbers: true
        },
        rules: {
          group: [
            {validator: validateGroup, type: 'object', trigger: 'change'},
          ],
          message: [
            {validator: validateMessage, type: 'object', trigger: 'change'}
          ],
        }
      }
    },
    methods: {
      onSubmit() {
        this.$refs['messagingForm'].validate((valid) => {
          if (valid) {
            this.startMessaging();
            this.handleClearGroup();
            this.handleClearMessage();
          } else {
            return false;
          }
        });
      },
      resetFields() {
        this.searchGroup = '';
        this.searchMessage = '';
        this.messagingForm.amount = 0;
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
      fetchMessages(queryString, cb) {
        HTTP.get(`entities/messages/?search=${queryString}`)
          .then(response => {
            if (response.status === 200) {
              this.fetchedMessages = response.data.results;
              cb(this.fetchedMessages);
            } else {
              this.$message({
                message: 'Error getting list of messages.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$message({
            message: 'Error getting list of messages.',
            type: 'error'
          });
        })
      },
      handleSelectGroup(item) {
        this.messagingForm.group = item;
        if (this.messagingForm.message) {
          this.fetchMaxMessagesAmount();
        }
      },
      handleSelectMessage(item) {
        this.messagingForm.message = item;
        this.fetchMaxMessagesAmount();
      },
      checkTaskStatus() {
        HTTP.get(`task-status/${this.taskId}/`)
          .then(response => {
              if ('success' in response.data) {
                if (response.data['success'] === true) {
                  this.$message({
                    message: 'Messaging finished!',
                    type: 'success'
                  });
                  this.loading = false;
                  this.handleClearGroup();
                  this.handleClearMessage();
                  this.resetFields();
                  this.$root.$emit('fetchBalance');
                } else {
                  this.$message({
                    message: response.data['error'],
                    type: 'error'
                  });
                  this.loading = false;
                  this.handleClearGroup();
                  this.handleClearMessage();
                  this.resetFields();
                  this.$root.$emit('fetchBalance');
                }
                clearInterval(this.intervalCheck);
                this.loading = false;
                this.intervalCheck = null;
                this.handleClearGroup();
                this.handleClearMessage();
                this.resetFields();
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error checking messaging status.',
            type: 'error'
          });
        });
      },
      handleClearGroup() {
        this.messagingForm.group = null;
        this.maxMessagesAmount = 0;
      },
      handleClearMessage() {
        this.messagingForm.message = null;
        this.maxMessagesAmount = 0;
      },
      fetchMaxMessagesAmount() {
        if (this.messagingForm.group) {
          this.fetchMaxMessages();
        }
      },
      fetchMaxMessages() {
        HTTP.post(`entities/contacts/get-not-messaged-count/`, {
          group_id: this.messagingForm.group.id,
          message_id: this.messagingForm.message.id,
        }).then(response => {
            if (response.status === 200) {
              if (response.data.count === 0) {
                this.maxMessagesAmount = 0;
                this.$notify({
                  title: 'Oops!',
                  message: `It seems like all users
                            from this group have been
                            already messaged this message or you
                            didn't scrape users from it yet.`,
                  type: 'warning'
                });
              } else if (response.data.count <= 500) {
                this.maxMessagesAmount = response.data.count;
              } else {
                this.maxMessagesAmount = 500;
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
      startMessaging() {
        this.loading = true;
        console.log(this.messagingForm)

        HTTP.post('actions/messaging/start', {
          group_id: this.messagingForm.group.id,
          message_id: this.messagingForm.message.id,
          use_system_numbers: this.messagingForm.useSystemNumbers,
          limit: this.messagingForm.amount
        }).then(response => {
          if (response.status === 200) {
            this.taskId = response.data['task_id'];
            this.intervalCheck = setInterval(function () {
              this.checkTaskStatus(true);
            }.bind(this), 1000);
          } else {
            this.$message({
              message: 'Failed to launch messaging.',
              type: 'error'
            });
            this.loading = false;
          }
        }).catch(e => {
          this.$message({
            message: 'Failed to launch messaging.',
            type: 'error'
          });
          this.loading = false;
        })
      },
      approximatePrice() {
        let price = this.messagingForm.useSystemNumbers ? 0.06 : 0.04;
        let result = this.messagingForm.amount * price;
        return result.toFixed(2);
      },
    },
    mounted() {
      this.checkIfUserHasOwnAccounts();
    }
  }
</script>

<style scoped>
  .el-steps {
    margin-top: 2%;
  }

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
