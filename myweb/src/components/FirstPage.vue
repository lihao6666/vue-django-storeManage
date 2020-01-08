<template>
  <div class="img1">
    <el-col :span="10" :offset="10">
    <p class="down">合肥工业大学软件学院</p>
    </el-col>
  </div>
</template>

<script>
export default {
  name: 'FirstPage',
  data () {
    return {
    }
  }
}
</script>

<style scoped>
  .img1{
    background: url("../picture/003.jpg");
    background-size: 100% 100%;
    height: 100%;
    position: center;
    width: 100%
  }
  .down {
    bottom: 50px;
    margin-left: auto;
    position: fixed;
  }
</style>
