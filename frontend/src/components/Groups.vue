<template>
  <div>
    <el-row type="flex" justify="start">
      <GroupsAddNew/>
    </el-row>
    <GroupsTable/>
  </div>
</template>


<script>
  import GroupsTable from './GroupsTable';
  import GroupsAddNew from './GroupsAddNew';

  export default {
    components: {
      GroupsTable, GroupsAddNew
    },
  }
</script>
