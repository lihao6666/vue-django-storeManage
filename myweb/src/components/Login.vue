<template>
  <div>
    <el-form :model="loginData" :rules="loginRules" ref="loginData" label-position="left" label-width="0px" class="login-container">
      <h3 class="title">系统登录</h3>
      <el-form-item prop="user_iden">
        <el-input type="text" v-model="loginData.user_iden" auto-complete="off" placeholder="账号" clearable >
          <template slot="prepend"><i class="el-icon-user" aria-hidden="true"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item prop="user_passwd">
        <el-input type="password" v-model="loginData.user_passwd" auto-complete="off" placeholder="密码" @keyup.enter.native="handleSubmit" clearable>
          <template slot="prepend"><i class="el-icon-key" aria-hidden="true"></i></template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" class="primary" @click.native.prevent="handleSubmit" :loading="isLogin" >登录</el-button>
      </el-form-item>
    </el-form>
    <div class="littlename">2020 © 艺朝艺夕仓储管理系统-V1.0</div>
  </div>
</template>

<script>
import {postAPI} from '../api/api'

export default {
  data () {
    return {
      isLogin: false,
      loginData: {
        user_iden: '',
        user_passwd: ''
      },
      loginRules: {
        user_iden: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        user_passwd: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      checked: true
    }
  },
  methods: {
    handleSubmit () {
      if (this.loginData.user_iden && this.loginData.user_passwd) {
        let _this = this
        this.isLogin = true
        let iden = localStorage.getItem('user_now_iden')
        if (iden) {
          this.$message.error('已经有用户登录了')
          this.isLogin = false
          return
        }
        postAPI('/base/login', this.loginData).then(function (res) {
          if (res.data.signal === '0') {
            _this.$message.success(res.data.message)
            localStorage.setItem('user_now_iden', _this.loginData.user_iden)
            localStorage.setItem('user', res.data)
            let roles = res.data.roles
            let n = 100
            let num = 0
            let str = String(Array(n > ('' + num).length ? (n - ('' + num).length + 1) : 0).join(0) + num)
            if (roles && roles.length > 0) {
              let n = roles[0][1].length || 26
              let num = 0
              str = String(Array(n > ('' + num).length ? (n - ('' + num).length + 1) : 0).join(0) + num)
              let strarr = str.split('')
              for (let i in roles) {
                let arr = roles[i][1].split('')
                for (let j = 0; j < arr.length; j++) {
                  if (strarr[j] === '0' || arr[j] === '3' || arr[j] === strarr[j]) {
                    strarr[j] = arr[j]
                  } else if (arr[j] !== '0') {
                    strarr[j] = '3'
                  }
                }
              }
              str = strarr.join('')
              console.log(str)
            }
            localStorage.setItem('user_power', str)
            _this.$router.push('/')
            _this.isLogin = false
          } else {
            _this.$message.error(res.data.message)
            _this.isLogin = false
          }
        }).catch(function (err) {
          console.log(err)
          _this.$message.error('登录失败')
          _this.isLogin = false
        })
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
