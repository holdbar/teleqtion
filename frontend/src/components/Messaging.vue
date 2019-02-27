<template>
  <el-tabs>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-d-arrow-right"></i> Start Messaging</span>
      Start Messaging Here
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-message"></i> My Messages</span>
      My Messages
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-circle-plus-outline"></i> New Message</span>
      <MessagingNewMessage/>
    </el-tab-pane>
  </el-tabs>
</template>


<script>
  import MessagingNewMessage from './MessagingNewMessage'

  export default {
    components: {
      MessagingNewMessage
    },
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>

</style>
