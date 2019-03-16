<template>
  <el-collapse v-model="activeTab" accordion>
    <el-collapse-item title="How to add your Telegram accounts to the system?" name="1">
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
    <el-collapse-item title="How to add Telegram Groups to the system?" name="2">
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
      <div>
        Scrapping - is a process of getting list of members of a Telegram group.
        After the group is scrapped, you can invite its members to other Telegram groups
        or send them private messages.
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
            If so, just click `Use my account` switch.
          </li>
          <li>
            Click `Scrape` button. Wait a little bit.
          </li>
          <li>
            Done! Now you can check and edit list of scrapped users at `Scrapped Users`
            tab.
          </li>
        </ol>
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to invite users to groups?" name="4">
      <div>
        <ol>
          <li>
            Go to "Inviting" tab.
          </li>
          <li>
            Start typing Source Group name and select the group you
            want to invite users from.
          </li>
          <li>
            Start typing Target Group name and select the group you
            want to invite users to.
          </li>
          <li>
            Set `Amount of users to invite`.
          </li>
          <li>
            Decide what you want: to `Use system accounts` or no.
            The main thing here is the price:
            if you enable using system account, you don't need to worry about
            anything - the system will handle everything for you. But the price per invite
            is 0.06$.
            But if you decide to use your own Telegram account (active and confirmed
            accounts from `My Accounts` tab) - price per invite is 0.04$.
          </li>
          <li>
            Now you are ready to go! Click `Start Inviting` and open your Target
            Group in the Telegram to see the results.
          </li>
        </ol>
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to send private messages to users?" name="5">
      <div>
        <ol>
          <li>
            Go to "Messaging" tab.
          </li>
          <li>
            If you don't have any messages yet, go to `New Message` and add a new one.
          </li>
          <li>
            Go to `Start Messaging` tab. Start typing group name,
            that you've already scrapped and select a group.
          </li>
          <li>
            Start typing message title to select message, that you want to sent
            to users of the chosen group.
          </li>
          <li>
            Set `Amount of users to send message to`.
          </li>
          <li>
            Decide what you want: to `Use system accounts` or no.
            The main thing here is the price:
            if you enable using system account, you don't need to worry about
            anything - the system will handle everything for you. But the price per send message
            is 0.06$.
            But if you decide to use your own Telegram account (active and confirmed
            accounts from `My Accounts` tab) - price per sent message is 0.04$.
          </li>
          <li>
            Now you are ready to go! Click `Start messaging`.
          </li>
        </ol>
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
