<template>
  <div>
    <el-menu mode="horizontal"
             class="topMenu"
             :default-active=$route.path
             :router=true>
      <el-submenu index="3">
        <template slot="title">Account</template>
        <el-menu-item index="" @click="passwordDialogVisible = true">Change Password</el-menu-item>
        <el-menu-item index="" @click="logoutDialogVisible = true">Logout</el-menu-item>
      </el-submenu>
      <el-menu-item index="/balance">
        Balance
      </el-menu-item>
      <el-menu-item index="" class="balanceTag">
        <el-tag v-if="this.balance > 0" type="success" :hit=true>{{ this.balance }} $</el-tag>
        <el-tag v-else type="warning" :hit=true>{{ this.balance }} $</el-tag>
      </el-menu-item>
    </el-menu>

    <el-dialog
      :visible.sync="logoutDialogVisible"
      center>
      <span slot="title">
        <i id="logoutIcon" class="el-icon-question"></i>
      </span>
      <div class="text-center">
        Do your really want to logout?
      </div>
      <div class="logout-checkbox text-center">
        <el-checkbox v-model="logoutAll">Logout from all devices</el-checkbox>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="logoutDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="logout">
          Yes, logout <i class="el-icon-d-arrow-right"></i>
        </el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="Change Password"
      :visible.sync="passwordDialogVisible"
      :before-close="closePasswordDialog"
      center>
      <el-form :model="passwordForm"
               label-position="top"
               :rules="passwordRules"
               ref="passwordForm">
        <el-form-item label="New Password" prop="password1">
          <el-input v-model="passwordForm.password1" autocomplete="off" show-password></el-input>
        </el-form-item>
        <el-form-item label="New Password Confirm" prop="password2">
          <el-input v-model="passwordForm.password2" autocomplete="off" show-password></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closePasswordDialog">Cancel</el-button>
        <el-button type="primary" @click="changePassword">Save</el-button>
      </span>
    </el-dialog>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validatePassword1 = (rule, value, callback) => {
        if (!this.passwordForm.password1) {
          callback(new Error('Please enter new password.'));
        }
        if (this.passwordForm.password1 && this.passwordForm.password2 &&
          this.passwordForm.password1 !== this.passwordForm.password2) {
          callback(new Error("Passwords didn't match."));
        }
        callback();
      };
      let validatePassword2 = (rule, value, callback) => {
        if (!this.passwordForm.password2) {
          callback(new Error('Please enter new password confirmation.'));
        }
        if (this.passwordForm.password1 && this.passwordForm.password2 &&
          this.passwordForm.password1 !== this.passwordForm.password2) {
          callback(new Error("Passwords didn't match."));
        }
        callback();
      };
      return {
        balance: 0,
        logoutDialogVisible: false,
        logoutAll: false,
        passwordDialogVisible: false,
        passwordForm: {
          password1: '',
          password2: ''
        },
        passwordRules: {
          password1: [
            {validator: validatePassword1, trigger: 'blur'},
          ],
          password2: [
            {validator: validatePassword2, trigger: 'blur'}
          ],
        },
        password1Error: '',
        password2Error: '',

      }
    },
    methods: {
      fetchBalance() {
        HTTP.get('auth/user/')
          .then(response => {
            if (response.status === 200) {
              this.balance = response.data.balance;
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error getting balance.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error getting balance.',
              type: 'error'
            });
          })
      },
      logout() {
        if (this.logoutAll) {
          HTTP.post('auth/logout/', {})
            .then(response => {
                if (response.status !== 200) {
                  this.$notify({
                    title: 'Error',
                    message: 'Error logging out.',
                    type: 'error'
                  });
                }
              }
            )
            .catch(e => {
              this.$notify({
                title: 'Error',
                message: 'Error logging out.',
                type: 'error'
              });
            });
        }
        localStorage.removeItem('token');
        window.location.href = 'http://localhost:8000/';
      },
      submitNewPassword() {
        HTTP.post('auth/password/change/', {
          new_password1: this.passwordForm.password1,
          new_password2: this.passwordForm.password2
        }).then(response => {
            if (response.status === 200) {
              this.$notify({
                title: 'Success',
                message: 'Password changed.',
                type: 'success'
              });
              this.closePasswordDialog();
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error changing password.',
                type: 'error'
              });
            }
          }
        ).catch(e => {

          if ('new_password1' in e.response.data) {
            var errors = '<ul>';
            for (let error of e.response.data.new_password1) {
              errors += `<li>${error}</li>`;
            }
            errors += '</ul>';
          }
          if ('new_password2' in e.response.data) {
            var errors = '<ul>';
            for (let error of e.response.data.new_password2) {
              errors += `<li>${error}</li>`;
            }
            errors += '</ul>';
          }
          this.$notify({
            title: 'Error',
            dangerouslyUseHTMLString: true,
            message: `Error changing password: ${errors}`,
            type: 'error'
          });
        });
      },
      changePassword() {
        this.$refs['passwordForm'].validate((valid) => {
          if (valid) {
            this.submitNewPassword();
          } else {
            return false;
          }
        });
      },
      closePasswordDialog() {
        this.$refs['passwordForm'].resetFields();
        this.passwordDialogVisible = false;
      }
    },
    mounted() {
      this.fetchBalance();
      setInterval(this.fetchBalance.bind(this), 60000);
      this.$root.$on('fetchBalance', () => {
        this.fetchBalance();
      });
    }
  }
</script>

<style scoped>
  .topMenu {
    transition: border-color .3s, background-color .3s, color .3s;
    border-bottom: solid 1px #e6e6e6;
    width: 100%;
  }

  .el-menu-item, .el-submenu {
    float: right;
  }

  .el-tag {
    font-size: 14px;
    font-weight: bold;
  }

  .balanceTag, .balanceTag.is-active {
    border-bottom: 0;
    cursor: default;
  }

  .text-center {
    text-align: center !important;
  }

  .logout-checkbox {
    margin: 2em 0;
  }

  #logoutIcon {
    font-size: 3em;
  }
</style>
