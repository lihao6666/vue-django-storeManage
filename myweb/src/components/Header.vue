<template>
  <div class="header">
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="collapseChage">
      <i v-if="!collapse" class="el-icon-s-fold"></i>
      <i v-else class="el-icon-s-unfold"></i>
    </div>
    <div class="logo">仓储管理系统</div>
    <div class="header-right">
      <div class="header-user-con">
        <!-- 用户头像 -->
        <div class="user-avator">
          <img src="../assets/logo.jpg"/>
        </div>
        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{username}}
                        <i class="el-icon-caret-bottom"></i>
                    </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
            <el-dropdown-item divided command="loginout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <!-- 修改弹出框 -->
    <el-dialog title="修改密码" :visible.sync="editVisible" width="30%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="100px">
          <el-form-item label="原密码">
            <el-input type="password" v-model="editform.old_password"></el-input>
          </el-form-item>
          <el-form-item label="新密码">
            <el-input type="password" v-model="editform.new_password"></el-input>
          </el-form-item>
          <el-form-item label="重复新密码">
            <el-input type="password" v-model="editform.again_password"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="14">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="changePassword">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>
<script>
import bus from './bus'
import {postAPI} from '../api/api'
export default {
  data () {
    return {
      collapse: false,
      fullscreen: false,
      name: 'Mars456',
      message: 2,
      editVisible: false,
      editform: {
        old_password: '',
        new_password: '',
        again_password: ''
      }
    }
  },
  computed: {
    username () {
      let username = localStorage.getItem('user_now_iden')
      if (username) {
        return username
      }
      return this.name
    }
  },
  methods: {
    // 用户名下拉菜单选择事件
    handleCommand (command) {
      if (command === 'loginout') {
        let _this = this
        postAPI('/base/loginExit', {}).then(function (res) {
          _this.$message.success(res.data.message)
          localStorage.clear()
          _this.$router.push('/login')
        }).catch(function (err) {
          console.log(err)
        })
      } else if (command === 'changePassword') {
        this.editVisible = true
      }
    },
    // 侧边栏折叠
    collapseChage () {
      this.collapse = !this.collapse
      bus.$emit('collapse', this.collapse)
    },
    // 修改密码
    changePassword () {
      if (!this.editform.old_password || !this.editform.new_password || !this.editform.again_password) {
        this.$message.error(`请填写完信息`)
        return
      }
      if (this.editform.new_password !== this.editform.again_password) {
        this.$message.error(`两次密码不一致`)
        return
      }
      this.$message.success(`修改密码成功`)
      this.editform.old_password = ''
      this.editform.new_password = ''
      this.editform.again_password = ''
      this.editVisible = false
    }
  },
  mounted () {
    if (document.body.clientWidth < 1500) {
      this.collapseChage()
    }
  }
}
</script>
<style scoped>
  .header {
    position: relative;
    box-sizing: border-box;
    width: 100%;
    height: 70px;
    font-size: 22px;
    color: #fff;
  }

  .collapse-btn {
    float: left;
    padding: 0 21px;
    cursor: pointer;
    line-height: 70px;
  }

  .header .logo {
    float: left;
    width: 250px;
    line-height: 70px;
  }

  .header-right {
    float: right;
    padding-right: 50px;
  }

  .header-user-con {
    display: flex;
    height: 70px;
    align-items: center;
  }

  .btn-fullscreen {
    transform: rotate(45deg);
    margin-right: 5px;
    font-size: 24px;
  }

  .btn-bell,
  .btn-fullscreen {
    position: relative;
    width: 30px;
    height: 30px;
    text-align: center;
    border-radius: 15px;
    cursor: pointer;
  }

  .btn-bell-badge {
    position: absolute;
    right: 0;
    top: -2px;
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background: #f56c6c;
    color: #fff;
  }

  .btn-bell .el-icon-bell {
    color: #fff;
  }

  .user-name {
    margin-left: 10px;
  }

  .user-avator {
    margin-left: 20px;
  }

  .user-avator img {
    display: block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .el-dropdown-link {
    color: #fff;
    cursor: pointer;
  }

  .el-dropdown-menu__item {
    text-align: center;
  }
</style>
