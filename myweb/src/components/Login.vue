<template>
  <div>
    <el-form :model="loginData" :rules="loginRules" ref="loginData" label-position="left" label-width="0px" class="login-container">
      <h3 class="title">系统登录</h3>
      <el-form-item prop="checkName">
        <el-input type="text" v-model="loginData.checkName" auto-complete="off" placeholder="账号" clearable >
          <template slot="prepend"><i class="el-icon-user" aria-hidden="true"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="checkPass">
        <el-input type="password" v-model="loginData.checkPass" auto-complete="off" placeholder="密码" @keyup.enter.native="handleSubmit" clearable>
          <template slot="prepend"><i class="el-icon-key" aria-hidden="true"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" class="primary" @click.native.prevent="handleSubmit" :loading="isLogin" >登录</el-button>
      </el-form-item>
    </el-form>
    <div class="littlename">2019 © 艺朝艺夕仓储管理系统-V1.0</div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isLogin: false,
      loginData: {
        checkName: '',
        checkPass: ''
      },
      loginRules: {
        checkName: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        checkPass: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      checked: true
    }
  },
  methods: {
    handleSubmit () {
      if (this.loginData.checkName) {
        this.$message.success('登录成功')
        localStorage.setItem('ms_username', this.loginData.checkName)
        this.$router.push('/')
      } else {
        this.$message.error('请输入账号和密码')
      }
    }
  }
}
</script>

<style scoped>
  .login-container {
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 180px auto 0px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }
  .title {
    margin: 0px auto 28px auto;
    text-align: center;
    color: #505458;
  }
  .littlename {
    text-align: center;
    margin:10px 0px;
    font-size: 12px;
  }
  .primary {
    width: 100%;
  }
</style>
