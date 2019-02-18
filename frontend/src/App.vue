<template>
  <div id="app">
    <el-container>
      <el-row :gutter="10">
        <el-col :md="6" :lg="4" class="hidden-sm-and-down sideMenu">
          <SideMenu/>
        </el-col>
        <el-col :sm="24" :md="18" :lg="20">
          <el-main>
            <router-view/>
          </el-main>
        </el-col>
      </el-row>
    </el-container>
  </div>
</template>

<script>
  import SideMenu from './components/SideMenu.vue'

  export default {
    name: 'App',
    components: {
      SideMenu,
    },
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Paytone+One');

  /*html {*/
  /*min-height: 100%;*/
  /*}*/

  body {
    min-height: 100vh;
    margin: 0;
  }

  .el-container {
    min-height: 100vh;

  }

  .el-row {
    width: 100%;
  }

  .el-menu {
    border-right: 0;
  }

  .sideMenu {
    transition: border-color .3s, background-color .3s, color .3s;
    border-right: solid 1px #e6e6e6;
    height: 100%;
    padding-right: 0 !important;

  }

  #app {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    min-height: 100vh;
  }
</style>
