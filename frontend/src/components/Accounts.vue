<template>
  <div>
    <el-row type="flex" justify="start">
      <AccountsAddNew/>
    </el-row>
    <AccountsTable/>
    <AccountsConfirm/>
  </div>
</template>


<script>
  import AccountsTable from './AccountsTable';
  import AccountsAddNew from './AccountsAddNew';
  import AccountsConfirm from './AccountsConfirm';

  export default {
    components: {
      AccountsTable, AccountsAddNew, AccountsConfirm
    },
  }
</script>
