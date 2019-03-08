<template>
  <el-tabs>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-d-arrow-right"></i> Start Messaging</span>
      <MessagingStart/>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-message"></i> My Messages</span>
      <MessagingList/>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-circle-plus-outline"></i> New Message</span>
      <MessagingNewMessage/>
    </el-tab-pane>
  </el-tabs>
</template>


<script>
  import MessagingNewMessage from './MessagingNewMessage'
  import MessagingList from './MessagingList'
  import MessagingStart from './MessagingStart'

  export default {
    components: {
      MessagingNewMessage, MessagingList, MessagingStart
    },
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>

</style>
