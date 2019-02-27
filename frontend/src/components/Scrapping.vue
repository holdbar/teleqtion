<template>
  <el-tabs>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-d-arrow-right"></i> Scrape</span>
      <ScrappingNew/>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-view"></i> Scrapped Users</span>
      <ScrappingResults/>
    </el-tab-pane>
  </el-tabs>

</template>


<script>
  import ScrappingNew from './ScrappingNew';
  import ScrappingResults from './ScrappingResults';

  export default {
    components: {
      ScrappingNew, ScrappingResults
    },
    data() {
      return {}
    },
    methods: {
      // handleTabClick(tab, event) {
      //   console.log(tab, event);
      // },
    }
  }
</script>

<style scoped>

</style>
