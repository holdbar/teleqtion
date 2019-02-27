<template>
  <el-menu mode="horizontal" class="topMenu" default-active="1">
    <el-submenu index="3">
      <template slot="title">Account</template>
      <el-menu-item index="3-1">Change Password</el-menu-item>
      <el-menu-item index="3-2">Logout</el-menu-item>
    </el-submenu>
    <el-menu-item index="2">
        Balance
    </el-menu-item>
     <el-menu-item index="1" class="balanceTag">
        <el-tag type="success" :hit=true>5.55 $</el-tag>
    </el-menu-item>
  </el-menu>

</template>


<script>
  export default {
    methods: {}
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
</style>
