<template>
  <el-form :inline=true
           :model="newAccount"
           :rules="rules"
           :hide-required-asterisk=true
           ref="newAccount"
           @submit.prevent.native="onSubmit"
           >
    <el-form-item label="Phone Number" prop="phone_number" @keyup.enter.native="onSubmit">
      <el-input v-model="newAccount.phone_number" @keyup.enter.native="onSubmit" placeholder="+1999999999999"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">Save</el-button>
    </el-form-item>
  </el-form>

</template>


<script>
  import {HTTP} from '../http-common';

  export default {
    data() {
      let validatePhoneNumber = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please input phone number'));
        } else {
          let expression = /^\+?\d{6,17}$/gi;
          let regex = new RegExp(expression);
          if (!value.match(regex)) {
            callback(new Error('Please input valid phone number.'));
          }
          callback();
        }
      };
      return {
        newAccount: {
          phone_number: '',
        },
        rules: {
          phone_number: [
            {validator: validatePhoneNumber, trigger: 'change'}
          ],
        }
      }
    },
    methods: {
      onSubmit() {
        this.$refs['newAccount'].validate((valid) => {
          if (valid) {
            this.postAccount();
            this.$refs['newAccount'].resetFields();
          } else {
            return false;
          }
        });
      },
      postAccount() {
        HTTP.post('telegram-accounts/', {
          phone_number: this.newAccount.phone_number,
        }).then(response => {
          if (response.status === 201) {
            this.$notify({
              title: 'Success',
              message: 'New Account added.',
              type: 'success'
            });
            this.$root.$emit('newAccountAdded', null, response);
            this.$root.$emit('confirmAccountShow', response.data['id']);

          } else {
            this.$notify({
              title: 'Error',
              message: 'Error adding account.',
              type: 'error'
            });
          }
        }).catch(e => {
          this.$notify({
            title: 'Error',
            message: 'Error adding account.',
            type: 'error'
          });
        })
      },
    }
  }
</script>

<style scoped>
  .el-form {
    margin-bottom: 50px;
  }
</style>
