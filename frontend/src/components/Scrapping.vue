<template>
  <el-tabs v-model="activeTab" @tab-click="handleTabClick">
    <el-tab-pane label="Scrape New" name="scrapeNew">
      <ScrappingNew/>
    </el-tab-pane>
    <el-tab-pane label="Results" name="results">
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
      return {
        activeTab: 'scrapeNew',
      }
    },
    methods: {
      handleTabClick(tab, event) {
        console.log(tab, event);
      },
    }
  }
</script>

<style scoped>

</style>
