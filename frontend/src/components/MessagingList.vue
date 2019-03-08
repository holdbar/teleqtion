<template>
  <div v-loading="loading">
    <el-row type="flex">
      <el-card v-for="message in this.messages"
               v-bind:data="message"
               v-bind:key="message.id"
               class="box-card"
               shadow="hover">
        <div slot="header" class="header">
          <b>{{ message.title }}</b>
          <div class="actions">
            <el-button class="actions-btn" icon="el-icon-delete" circle
                       @click="handleDelete(message.id)"></el-button>
          </div>
        </div>

        <div class="text item">
          <el-tooltip v-if="message.text.length > 250" :content="message.text" placement="bottom" effect="light">
            <p v-html="message.text.slice(0,250)"></p>
          </el-tooltip>
          <p v-else v-html="message.text"></p>
          <h2 v-if="message.file">
            <el-tooltip class="item" effect="dark" content="message attachment" placement="top">
              <a target="_blank" :href="message.file"><i class="el-icon-upload"></i></a>
            </el-tooltip>
          </h2>
          <el-tag v-if="message.link_preview">Link Preview <i class="el-icon-success"></i></el-tag>
          <el-tag v-else type="info">Link Preview <i class="el-icon-error"></i></el-tag>
        </div>


        <div class="bottom">

          <time class="time">
            <i class="el-icon-time"></i>
            {{ message.updated_at | formatDate }}
          </time>
        </div>
      </el-card>
    </el-row>
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
        loading: false,
        total_pages: 1,
        messages: [],
      }
    },
    methods: {
      fetchMessages(page) {
        this.loading = true;
        if (page === undefined) {
          page = 1;
        }
        HTTP.get(`entities/messages/?page=${page}`)
          .then(response => {
            this.messages = response.data.results;
            this.total_pages = response.data.count;
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error getting list of messages.',
              type: 'error'
            });
          }).finally(() => (this.loading = false));
      },
      handleCurrentPageChange(val) {
        this.fetchMessages(val);
      },
      handleDelete(messageId) {
        this.$confirm(
          'Are you sure you want to delete this message?',
          'Warning', {
            confirmButtonText: 'Yes',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }).then(() => {
          this.deleteMessage(messageId)
        }).catch(() => {
        });
      },
      deleteMessage(messageId) {
        HTTP.delete(`entities/messages/${messageId}`)
          .then(response => {
            if (response.status === 204) {
              this.$notify({
                title: 'Success',
                message: 'Message deleted.',
                type: 'success'
              });
              this.fetchMessages();
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error deleting message.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.errors.push(e);
            this.$notify({
              title: 'Error',
              message: 'Error deleting message.',
              type: 'error'
            });
          })
      }
    },
    mounted() {
      this.fetchMessages();
      this.$root.$on('newMessageAdded', () => {
        this.fetchMessages();
      });
    }
  }
</script>

<style scoped>
  .el-row {
    flex-wrap: wrap;
  }

  .header {
    text-align: left;
    line-height: 30px;
  }

  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .actions {
    float: right;
    padding-bottom: 30px;
  }

  .actions-btn {
    padding: 7px 7px;
    margin-left: 3px;
  }

  .box-card {
    width: 21em;
    margin: 1em;
  }
</style>
