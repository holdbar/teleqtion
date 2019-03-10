<template>
  <el-collapse v-model="activeTab" accordion>
    <el-collapse-item title="How to add your Telegram accounts?" name="1">
      <video src="http://static.smartisanos.cn/common/video/t1-ui.mp4" controls></video>
    </el-collapse-item>
    <el-collapse-item title="How to add Telegram Groups?" name="2">
      <div>Operation feedback: enable the users to clearly perceive their operations by style updates and interactive
        effects;
      </div>
      <div>Visual feedback: reflect current state by updating or rearranging elements of the page.</div>
    </el-collapse-item>
    <el-collapse-item title="How to start scrapping?" name="3">
      <div>Simplify the process: keep operating process simple and intuitive;</div>
      <div>Definite and clear: enunciate your intentions clearly so that the users can quickly understand and make
        decisions;
      </div>
      <div>Easy to identify: the interface should be straightforward, which helps the users to identify and frees them
        from memorizing and recalling.
      </div>
    </el-collapse-item>
    <el-collapse-item title="How to start inviting?" name="4">
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
        activeTab: '1'
      };
    }
  }
</script>

<style scoped>
  .el-collapse-item__content > video {
    max-height: 300px;
  }
</style>
