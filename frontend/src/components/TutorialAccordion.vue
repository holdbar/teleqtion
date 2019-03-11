<template>
  <el-collapse v-model="activeTab" accordion>
    <el-collapse-item title="How to add your Telegram accounts?" name="1">
      <video src="http://static.smartisanos.cn/common/video/t1-ui.mp4" controls></video>
      <div>
        <ol>
          <li>
            Go to "My Accounts" tab.
          </li>
          <li>
            Enter phone number to the form and click "Add".
          </li>
          <li>
            You'll see a modal window. Click `Request Code`. The phone number will receive
            a confirm code from Telegram.
          </li>
          <li>
            Enter the code, you've received, and click `Confirm`.
          </li>
          <li>
            Done! Now you can use this account for scrapping, messaging and inviting.
          </li>
        </ol>
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to add Telegram Groups?" name="2">
      <video src="http://static.smartisanos.cn/common/video/t1-ui.mp4" controls></video>
      <div>
        <ol>
          <li>
            Go to "Telegram Groups" tab.
          </li>
          <li>
            Enter group title (group identificator, only you will see it).
          </li>
          <li>
            If the group is public, enter group username. Else - enter group join link.
          </li>
          <li>
            Click `Save`.
          </li>
          <li>
            Done! Now you can scrape users from this group,
            send them private messages or invite them to other groups.
          </li>
        </ol>
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to scrape users from groups?" name="3">
      <video src="http://static.smartisanos.cn/common/video/t1-ui.mp4" controls></video>
      <div>
        <ol>
          <li>
            Go to "Scrapping" tab.
          </li>
          <li>
            Start typing your group name and select the group you want.
          </li>
          <li>
            If the group is private, you may want to use your own account
            (that is already a member or an administrator of the group).
            If so, just click `Use my account` switch. You'll see

          </li>
          <li>
            Click `Save`.
          </li>
          <li>
            Done! Now you can scrape users from this group,
            send them private messages or invite them to other groups.
          </li>
        </ol>
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to invite users to groups?" name="4">
      <div>Decision making: giving advices about operations is acceptable, but do not make decisions for the users;
      </div>
      <div>Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or
        terminating current operation.
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to send private messages to users?" name="5">
      <div>Decision making: giving advices about operations is acceptable, but do not make decisions for the users;
      </div>
      <div>Controlled consequences: users should be granted the freedom to operate, including canceling, aborting or
        terminating current operation.
      </div>
    </el-collapse-item>
  </el-collapse>
</template>


<script>
  export default {
    data() {
      return {
        activeTab: ''
      };
    }
  }
</script>

<style scoped>
  .el-collapse-item__content > video {
    max-height: 300px;
  }

  .el-collapse-item__content > div {
    text-align: left;
  }
</style>
