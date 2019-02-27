<template>
  <el-row>
    <el-menu
      class="el-menu-vertical"
      :default-active=$route.path
      :router=true>
      <div class="logo">
        <span>TeleQtion</span>
      </div>
      <el-menu-item index="/">
        <i class="el-icon-menu"></i>
        <span>Dashboard</span>
      </el-menu-item>
      <el-menu-item index="/accounts">
        <i class="el-icon-location-outline"></i>
        <span>My Accounts</span>
      </el-menu-item>
      <el-menu-item index="/groups">
        <i class="el-icon-tickets"></i>
        <span>Telegram Groups</span>
      </el-menu-item>
      <el-menu-item index="/scrapping">
        <i class="el-icon-zoom-in"></i>
        <span>Scrapping</span>
      </el-menu-item>
      <el-menu-item index="/inviting">
        <i class="el-icon-circle-check-outline"></i>
        <span>Inviting</span>
      </el-menu-item>
      <el-menu-item index="/messaging">
        <i class="el-icon-message"></i>
        <span>Messaging</span>
      </el-menu-item>
    </el-menu>
  </el-row>
</template>


<script>
  export default {
    methods: {}
  }
</script>

<style scoped>
  .el-row {
    text-align: left;
  }
  .logo {
    font-family: 'Paytone One', sans-serif;
    font-size: 16px;
    margin: 10px 20px;
    text-align: center;
  }
</style>
