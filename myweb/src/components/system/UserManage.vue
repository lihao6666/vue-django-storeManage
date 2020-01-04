<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 用户管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" icon="el-icon-plus" @click="handleAlter" class="alter-button">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="user_name" sortable label="姓名" align="center"></el-table-column>
        <el-table-column prop="username" sortable label="工号" align="center"></el-table-column>
        <el-table-column prop="user_phone_number" sortable label="手机号" align="center"></el-table-column>
        <el-table-column prop="email" sortable label="邮箱" align="center"></el-table-column>
        <el-table-column prop="area_name" sortable label="区域" :filters="area_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="user_departments" sortable label="部门" :filters="user_dpmSet"
                         :filter-method="filterMore" align="center">
          <template slot-scope="scope">
            <el-tag v-for="item in scope.row.user_departments" v-bind:key="item" :type="'success'">{{item}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_roles" sortable label="角色" :filters="user_rolesSet"
                         :filter-method="filterMore" align="center">
          <template slot-scope="scope">
            <el-tag v-for="item in scope.row.user_roles" v-bind:key="item" :type="'success'">{{item}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_creator" sortable label="创建人" :filters="user_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="date_joined" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-unlock"
              class="red"
              @click="handleStop(scope.row)"
              v-if="scope.row.is_active"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart( scope.row)"
              v-else
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
          <el-pagination
            @current-change="handlePageChange"
            @size-change="handleSizeChange"
            :page-sizes="[5, 10, 20, 50, 100, 200, 500]"
            :current-page="query.pageIndex"
            :page-size="query.pageSize"
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="pageTotal">
          </el-pagination>
      </div>
    </div>

    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="alterVisible" width="30%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :rules="rules" :model="form" label-width="80px"  class="form" >
          <el-row>
            <el-form-item label="姓名" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.user_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="工号" class="inputs" align="left" prop="username">
              <el-col :span="10">
                <el-input v-model="form.username" @input="form.username=inputnum(form.username)"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="手机号" class="inputs" align="left" prop="user_phone_number">
              <el-col :span="10">
                <el-input v-model="form.user_phone_number" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="邮箱" class="inputs" align="left" prop="email">
              <el-col :span="10">
                <el-input v-model="form.email"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="区域"  align="left">
              <el-select v-model="form.area_name" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in area_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="部门"  align="left">
              <el-select v-model="form.user_departments" multiple placeholder="请选择部门" class="option" >
                <el-option
                  v-for="item in dpm_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="角色"  align="left">
              <el-select v-model="form.user_roles" multiple placeholder="请选择角色" class="option">
                <el-option
                  v-for="item in role_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="13">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="5">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="30%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="80px"  class="form" :rules="rules">
          <el-row>
            <el-form-item label="姓名" class="inputs" align="left" prop="user_name">
              <el-col :span="10">
                <el-input v-model="editform.user_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="工号" class="inputs" align="left" prop="username" >
              <el-col :span="10">
                <el-input v-model="editform.username" @input="editform.username=inputnum(editform.username)"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="手机号" class="inputs" align="left" prop="user_phone_number">
              <el-col :span="10">
                <el-input v-model="editform.user_phone_number"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="邮箱" class="inputs" align="left" prop="email">
              <el-col :span="10">
                <el-input v-model="editform.email"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="区域"  align="left">
              <el-select v-model="editform.area_name" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in area_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="部门"  align="left">
              <el-select v-model="editform.user_departments" multiple placeholder="请选择部门" class="option" >
                <el-option
                  v-for="item in dpm_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="角色"  align="left">
              <el-select v-model="editform.user_roles" multiple placeholder="请选择角色">
                <el-option
                  v-for="item in role_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="13">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      rules: {
        email: [{
          required: true,
          message: '请输入邮箱地址',
          trigger: 'blur'
        },
        {
          type: 'email',
          message: '请输入正确的邮箱地址',
          trigger: ['blur', 'change']
        }
        ],
        user_phone_number: [{
          required: true,
          message: '请输入手机号',
          trigger: 'blur'
        },
        {
          message: '请输入正确的手机号',
          pattern: /^1[34578]\d{9}$/,
          trigger: ['blur', 'change']
        }],
        username: [{
          required: true,
          message: '请输入工号',
          trigger: 'blur'
        }]
      },
      role_options: [],
      area_options: [],
      dpm_options: [],
      search: '',
      form: {
        user_name: '',
        username: '',
        email: '',
        area_name: '',
        user_phone_number: '',
        user_departments: [],
        user_roles: []
      },
      username: '',
      editform: {
        user_name: '',
        username: '',
        email: '',
        area_name: '',
        user_phone_number: '',
        user_departments: [],
        user_roles: []
      },
      tableData: [],
      tableDataNew: [],
      user_rolesSet: [],
      area_nameSet: [],
      user_dpmSet: [],
      user_creatorSet: [],
      multipleSelection: [],
      delroles: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      this.getroles()
      let _this = this
      getAPI('/base/users').then(function (res) {
        _this.user_rolesSet = []
        _this.area_nameSet = []
        _this.user_dpmSet = []
        _this.user_creatorSet = []
        _this.tableData = res.data.users
        let areaset = new Set()
        let creatorset = new Set()
        let dpmset = new Set()
        let roleset = new Set()
        for (let i in _this.tableData) {
          _this.tableData[i].user_roles = res.data.roles[i]
          _this.tableData[i].user_departments = res.data.departments[i]
          areaset.add(_this.tableData[i]['area_name'])
          for (let j in _this.tableData[i]['user_departments']) {
            dpmset.add(_this.tableData[i]['user_departments'][j])
          }
          for (let j in _this.tableData[i]['user_roles']) {
            roleset.add(_this.tableData[i]['user_roles'][j])
          }
          creatorset.add(_this.tableData[i]['user_creator'])
        }
        console.log(_this.tableData)
        _this.find()
        for (let i of areaset) {
          _this.area_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.user_creatorSet.push({
            text: i,
            value: i
          })
        }
        for (let i of dpmset) {
          _this.user_dpmSet.push({
            text: i,
            value: i
          })
        }
        for (let i of roleset) {
          _this.user_rolesSet.push({
            text: i,
            value: i
          })
        }
        _this.pageTotal = res.data.users.length
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 表格每行的class样式
    tableRowClassName ({row, rowIndex}) {
      this.pageTotal = rowIndex + 1
      if (rowIndex >= (this.query.pageIndex - 1) * this.query.pageSize && rowIndex < this.query.pageIndex * this.query.pageSize) {
        return ''
      }
      return 'tableRowDisplay'
    },
    // 修改数量
    inputnum (num) {
      num = num.replace(/[^\d]/g, '')
      return num
    },
    // 表格下拉筛选
    filter (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    filterMore (value, row, column) {
      const property = column['property']
      if (row[property].indexOf(value) >= 0) {
        return true
      }
      return false
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        String(data.user_name).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.username).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_phone_number).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.area_name).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.email).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.user_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 获取列表
    getroles () {
      let _this = this
      getAPI('/base/userNew').then(function (res) {
        let n = res.data.max_iden.length
        let num = parseInt(res.data.max_iden) + 1
        _this.username = String(Array(n > num ? (n - ('' + num).length + 1) : 0).join(0) + num)
        _this.role_options = res.data.roles
        _this.area_options = res.data.areas
        _this.dpm_options = res.data.departments
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
      this.form.username = this.username
    },
    // 一键清除新增表单
    clearform () {
      this.form.user_name = ''
      this.form.username = ''
      this.form.email = ''
      this.form.area_name = ''
      this.form.user_phone_number = ''
      this.form.user_departments = []
      this.form.user_roles = []
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.is_active = false
          console.log(row)
          postAPI('/base/userStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
            } else {
              _this.$message.error(res.data.message)
              row.is_active = true
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.is_active = true
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.is_active = true
          console.log(row)
          postAPI('/base/userStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
            } else {
              _this.$message.error(res.data.message)
              row.is_active = false
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.is_active = false
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消启用'
          })
        })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.user_name = row.user_name
      this.editform.username = row.username
      this.editform.id = row.id
      this.editform.email = row.email
      this.editform.area_name = row.area_name
      let role = []
      for (let i in row.user_roles) {
        role.push(row.user_roles[i])
      }
      this.editform.user_roles = role
      this.editform.user_phone_number = row.user_phone_number
      let dpm = []
      for (let i in row.user_departments) {
        dpm.push(row.user_departments[i])
      }
      this.editform.user_departments = dpm
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      if (!this.editform.user_name || !this.editform.username || !this.editform.email || !this.editform.area_name || !this.editform.user_phone_number) {
        this.$message.error(`请填写完信息`)
        return
      }
      let email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
      if (!this.rules.user_phone_number[1].pattern.test(this.editform.user_phone_number) || !email.test(this.editform.email)) {
        this.$message.error(`请填写正确格式`)
        return
      }
      let _this = this
      console.log(this.editform)
      postAPI('/base/userUpdate', this.editform).then(function (res) {
        console.log(res.data)
        if (res.data.signal === 0) {
          _this.$message.success(`修改成功`)
          _this.getData()
          _this.editVisible = false
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`修改失败`)
      })
    },
    // 保存新增
    saveAlter () {
      console.log(this.form.user_roles)
      if (!this.form.user_name || !this.form.username || !this.form.email || !this.form.area_name || !this.form.user_phone_number) {
        this.$message.error(`请填写完信息`)
        return
      }
      let email = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/
      if (!this.rules.user_phone_number[1].pattern.test(this.form.user_phone_number) || !email.test(this.form.email)) {
        this.$message.error(`请填写正确格式`)
        return
      }
      this.form.role_power = ''
      this.form.password = this.form.username
      console.log(this.form)
      let _this = this
      postAPI('/base/userAdd', this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.getData()
          _this.clearform()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`新增失败`)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    }
  }
}
</script>

<style>
  .el-row-button-save {
    top: 15px;
  }
  .tableRowDisplay {
    display: none;
  }
</style>

<style scoped>
  .handle-box {
    margin-bottom: 20px;
    position: relative;
  }
  .input-search {
    width: 50%;
  }
  .alter-button{
    position: absolute;
    right:0;
  }
  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: GREEN;
  }
  .inputs {
    width: 150%;
  }
</style>
