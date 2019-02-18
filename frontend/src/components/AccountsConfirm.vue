<template>
  <el-dialog title="Confirm Account"
             center
             :visible.sync="confirmFormVisible"
             :before-close="onClose"
             >
    <!-- Steps Bar -->
    <el-steps :active="activeStep" finish-status="success" align-center>
      <el-step title="Request Code"></el-step>
      <el-step title="Confirm"></el-step>
    </el-steps>
    <div v-loading="dialogLoading"></div>

    <!-- Step 1 -->
    <div v-show="activeStep === 0" style="text-align: center">
      <p>To confirm an account, press "Request code" button.</p>
      <p>You'll receive a confirmation code via SMS.</p>
    </div>
    <span slot="footer" class="dialog-footer" v-show="activeStep === 0">
        <el-button @click="onClose">Cancel</el-button>
        <el-button @click="haveCode">I already have code</el-button>
        <el-button type="primary" @click="requestCode">Request code</el-button>
      </span>

    <!-- Step 2 -->
    <transition name="el-zoom-in-top">
      <el-form :model="confirmAccount" v-show="activeStep === 1"
               :rules="rules"
               :hide-required-asterisk=true
               ref="confirmAccountForm"
               @submit.prevent.native="onSubmit">
        <el-form-item label="Code from SMS" prop="code">
          <el-input v-model="confirmAccount.code" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
    </transition>

    <span slot="footer" class="dialog-footer" v-show="activeStep === 1">
      <el-button @click="onClose">Cancel</el-button>
      <el-button type="primary" @click="onSubmit">Confirm</el-button>
    </span>

  </el-dialog>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validateConfirmCode = (rule, value, callback) => {
        if (!value) {
          callback(new Error('Please input code from SMS'));
        } else {
          let expression = /^\d{4,10}$/gi;
          let regex = new RegExp(expression);
          if (!value.match(regex)) {
            callback(new Error('Please input valid code.'));
          }
          callback();
        }
      };
      return {
        intervalCheck: null,
        taskId: null,

        activeStep: 0,
        dialogLoading: false,
        confirmFormVisible: false,

        confirmAccount: {
          accountId: '',
          code: ''
        },

        rules: {
          code: [
            {validator: validateConfirmCode, trigger: 'change'},
          ],
        }
      }
    },
    methods: {
      onSubmit() {
        this.$refs['confirmAccountForm'].validate((valid) => {
          if (valid) {
            this.postConfirmAccount();
          } else {
            return false;
          }
        });
      },
      onClose() {
        this.confirmFormVisible = false;
        this.dialogLoading = false;
        this.activeStep = 0;
        this.$refs['confirmAccountForm'].resetFields();
      },
      requestCode() {
        this.dialogLoading = true;
        HTTP.post('telegram-accounts/code-request/', {
          id: this.confirmAccount.accountId,
        }).then(response => {
          if (response.status === 200) {
            this.taskId = response.data['task_id'];
            this.intervalCheck = setInterval(function () {
              this.checkTaskStatus();
            }.bind(this), 1000);
          } else {
            this.$message({
              message: 'Error sending SMS code.',
              type: 'error'
            });
            this.onClose();
          }
        }).catch(e => {
          this.$message({
            message: 'Error sending SMS code.',
            type: 'error'
          });
          this.onClose();
        });
      },
      haveCode() {
        this.activeStep++;
      },
      postConfirmAccount() {
        this.dialogLoading = true;
        HTTP.post('telegram-accounts/confirm/', {
          id: this.confirmAccount.accountId,
          code: this.confirmAccount.code,
        }).then(response => {
          if (response.status === 200) {
            this.taskId = response.data['task_id'];
            this.intervalCheck = setInterval(function () {
              this.checkTaskStatus(true);
            }.bind(this), 1000);
          } else {
            this.$message({
              message: 'Error confirming account.',
              type: 'error'
            });
            this.onClose();
          }
        }).catch(e => {
          this.$message({
            message: 'Error confirming account.',
            type: 'error'
          });
          this.onClose();
        })
      },
      checkTaskStatus(closeOnSuccess) {
        HTTP.get(`task-status/${this.taskId}/`)
          .then(response => {
              if ('success' in response.data) {
                if (response.data['success'] === true) {
                  this.activeStep++;
                  this.$message({
                    message: 'Success!',
                    type: 'success'
                  });
                  this.$root.$emit('accountConfirmed');
                  if (closeOnSuccess) {
                    this.onClose();
                  }
                } else {
                  this.$message({
                    message: response.data['error'],
                    type: 'error'
                  });
                  this.onClose();
                }
                clearInterval(this.intervalCheck);
                this.dialogLoading = false;
                this.intervalCheck = null;
              }
            }
          ).catch(e => {
          this.$message({
            message: 'Error checking process status.',
            type: 'error'
          });
        });

      }
    },
    mounted() {
      this.$root.$on('confirmAccountShow', (accountId) => {
        this.confirmAccount.accountId = accountId;
        this.confirmFormVisible = true;
      });
    }
  }
</script>

<style scoped>

</style>
