<template>
  <div>
    <vue-editor
      :editorToolbar="customToolbar"
      v-model="content"/>
    <el-switch
      v-model="linkPreview"
      active-text="Enable Link Preview"/>
    <el-row>
      <el-button type="primary" @click="">Save</el-button>
    </el-row>
  </div>
</template>


<script>
  import {VueEditor} from 'vue2-editor'

  export default {
    components: {
      VueEditor
    },
    data() {
      return {
        linkPreview: true,
        content: '<p>Write here your message.</p>',
        customToolbar: [
          ['bold', 'italic'],
          ['link'],
          ['blockquote', 'code-block'],
          ['clean'],
        ]
      }
    },
    methods: {
      saveMessage() {
        console.log(this.content);
      }
    }
  }
</script>

<style scoped>
  .el-switch {
    margin: 2% 0;
  }
</style>
