<template>
  <div>
    <label class="el-form-item__label">Message Title</label>
    <el-input placeholder="Message Title (only you will see this)"
              v-model="messageTitle"></el-input>

    <vue-editor
      :editorToolbar="customToolbar"
      v-model="content"/>
    <div class="upload">
      <el-upload action=""
                 :auto-upload="false"
                 :multiple="false"
                 :limit="1"
                 :on-exceed="handleFileLimitExceed"
                 :on-change="handleFileChange"
                 :on-remove="handleFileRemove">
        <el-button slot="trigger" size="small" type="primary" plain icon="el-icon-upload2">select files</el-button>
        <div class="el-upload__tip" slot="tip">
          select file you want to send with the message (file size must be less than 5mb)
        </div>
      </el-upload>
    </div>
    <el-switch
      v-model="linkPreview"
      active-text="Enable Link Preview"/>
    <el-row>
      <el-button type="primary" @click="submitMessage">Save</el-button>
    </el-row>
  </div>
</template>


<script>
  import {VueEditor} from 'vue2-editor'
  import {HTTP} from '../http-common';

  export default {
    components: {
      VueEditor
    },
    data() {
      return {
        messageTitle: '',
        linkPreview: true,
        content: '<p>Write here your message.</p>',
        customToolbar: [
          ['bold', 'italic'],
          ['link'],
          ['blockquote', 'code-block'],
          ['clean'],
        ],
        file: null
      }
    },
    methods: {
      submitMessage() {
        if (!this.messageTitle) {
          this.$notify({
            title: 'Error',
            message: 'Please, set title for your message.',
            type: 'error'
          });
          return;
        }
        if (this.file) {
          var post_data = new FormData();
          post_data.append('file', this.file.raw);
          post_data.append('title', this.messageTitle);
          post_data.append('text', this.content);
          post_data.append('link_preview', this.linkPreview);
          var headers = {'Content-Type': 'multipart/form-data'};
        } else {
          var post_data = {
            title: this.messageTitle,
            text: this.content,
            link_preview: this.linkPreview
          };
          var headers = {};
        }

        HTTP.post(
          'entities/messages/', post_data,
          {headers: headers}
        )
          .then(response => {
            if (response.status === 201) {
              this.$notify({
                title: 'Success',
                message: 'New Message added.',
                type: 'success'
              });
              this.$root.$emit('newMessageAdded')
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error adding message.',
                type: 'error'
              });
            }
          })
          .catch(e => {
            this.$notify({
              title: 'Error',
              message: 'Error adding message.',
              type: 'error'
            });
          })
      },
      handleFileLimitExceed() {
        this.$message('Max number of attachments: 1.');
      },
      handleFileChange(file, filelist) {
        const checkFileSize = file.size / 1024 / 1024 < 5;
        if (!checkFileSize) {
          this.$message.error('File size can not exceed 5MB!');
          this.file = null;
        } else {
          this.file = file;
        }
      },
      handleFileRemove() {
        this.file = null;
      },
    }
  }
</script>

<style scoped>
  .el-switch {
    margin: 2% 0;
  }

  .upload {
    margin-top: 2em;
  }

  .el-input {
    margin-bottom: 3em;
  }
</style>
