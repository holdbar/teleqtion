<template>
  <el-form :inline=true
           :model="newGroup"
           :rules="rules"
           :hide-required-asterisk=true
           ref="newGroup"
           @keyup.enter.native="onSubmit">
    <el-form-item label="Title" prop="title">
      <el-input v-model="newGroup.title"></el-input>
    </el-form-item>
    <el-form-item label="Group Username" prop="username">
      <el-input v-model="newGroup.username"></el-input>
    </el-form-item>
    <el-form-item label="Join Link" prop="joinLink">
      <el-input v-model="newGroup.joinLink" placeholder="https://t.me/my_group"></el-input>
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
      let validateUsername = (rule, value, callback) => {
        if (this.newGroup.username === '' && this.newGroup.joinLink === '') {
          callback(new Error('Please input group username or join link.'));
        } else {
          callback();
        }
      };
      let validateJoinLink = (rule, value, callback) => {
        if (this.newGroup.username === '' && this.newGroup.joinLink === '') {
          callback(new Error('Please input group username or join link.'));
        } else {
          let expression = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/gi;
          let regex = new RegExp(expression);
          if (this.newGroup.joinLink !== '' && !this.newGroup.joinLink.match(regex)) {
            callback(new Error('Please input valid join link.'));
          }
          callback();
        }
      };
      return {
        newGroup: {
          title: '',
          username: '',
          joinLink: '',
        },
        rules: {
          title: [
            {required: true, message: 'Please input Title', trigger: 'blur'},
            {min: 2, max: 255, message: 'Length should be 2 to 255', trigger: 'blur'}
          ],
          username: [
            {validator: validateUsername, trigger: 'blur'}
          ],
          joinLink: [
            {validator: validateJoinLink, trigger: 'blur'}
          ],
        }
      }
    },
    methods: {
      onSubmit() {
        this.$refs['newGroup'].validate((valid) => {
          if (valid) {
            this.postGroup();
            this.$refs['newGroup'].resetFields();
          } else {
            return false;
          }
        });
      },
      postGroup() {
        HTTP.post('entities/groups/', {
          title: this.newGroup.title,
          username: this.newGroup.username,
          join_link: this.newGroup.joinLink,
        })
          .then(response => {
            if (response.status === 201) {
              this.$notify({
                title: 'Success',
                message: 'New Group added.',
                type: 'success'
              });
              this.$root.$emit('newGroupAdded', null, response)
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error adding group.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.errors.push(e);
            this.$notify({
              title: 'Error',
              message: 'Error adding group.',
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
