<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 角色管理
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
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="角色描述：">
                <span>{{ props.row.role_description }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="role" sortable label="角色" :filters="role_roleSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="role_creator" sortable label="创建人" :filters="role_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="role_createDate" sortable label="创建日期" align="center"></el-table-column>
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
             v-if="scope.row.role_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.role_status===0"
            >启用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handlePower(scope.row)"
            >授权
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="40%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="80px" >
          <el-row>
            <el-form-item label="角色"  align="left">
              <el-col :span="10">
                <el-input v-model="form.role" class="name"></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="角色描述" align="left">
              <el-input type="textarea" class="textarea" v-model="form.role_description"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="16">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="3">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="40%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="80px">
          <el-form-item label="角色">
            <el-input v-model="editform.role"></el-input>
          </el-form-item>
          <el-form-item label="角色描述" align="left">
            <el-input type="textarea" class="textarea" v-model="editform.role_description"
                      placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
          </el-form-item>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="16">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="3">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <!-- 授权弹出框 -->
    <el-dialog title="授权" :visible.sync="powerVisible" width="40%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closeRolePower">
      <RolePower ref="RolePower" :powerform="powerform" @closePower="closePower"></RolePower>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="16">
          <el-button @click="closeRolePower">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="3">
          <el-button type="primary" @click="savePower">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
import RolePower from './RolePower'
export default {
  name: 'test',
  components: {
    RolePower
  },
  data () {
    return {
      manager: 'XXX',
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        role_description: '',
        role: ''
      },
      editform: {
        role_description: '',
        role: ''
      },
      powerform: {},
      tableData: [],
      tableDataNew: [],
      role: '',
      multipleSelection: [],
      role_creatorSet: [],
      role_roleSet: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      powerVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      getAPI('/base/roles').then(function (res) {
        if (!res.data.roles) {
          return
        }
        _this.role_creatorSet = []
        _this.role_roleSet = []
        _this.tableData = res.data.roles
        _this.pageTotal = res.data.roles.length
        _this.find()
        console.log(res.data)
        let roleset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          roleset.add(_this.tableData[i]['role'])
          creatorset.add(_this.tableData[i]['role_creator'])
        }
        for (let i of roleset) {
          _this.role_roleSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.role_creatorSet.push({
            text: i,
            value: i
          })
        }
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
    // 表格下拉筛选
    filter (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        String(data.role).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.role_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.role_description).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.role_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 一键清除新增表单
    clearform () {
      this.form.role = ''
      this.form.role_description = ''
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          row.role_status = 0
          let _this = this
          postAPI('/base/roleStatus', row).then(function (res) {
            console.log(res.data)
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.role_status = 1
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.role_status = 1
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
          row.role_status = 1
          let _this = this
          postAPI('/base/roleStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.role_status = 0
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.role_status = 0
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
      this.editform.role_description = row.role_description
      this.editform.role = row.role
      this.editform.role_status = row.role_status
      this.editform.role_power = row.role_power
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      if (!this.editform.role) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/roleUpdate', this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`修改成功`)
          _this.editVisible = false
          _this.getData()
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
      if (!this.form.role) {
        this.$message.error(`请填写完信息`)
        return
      }
      let data = {
        'role': this.form.role,
        'role_power': '00000000000000000000000000',
        'role_description': this.form.role_description,
        'role_status': 0,
        'role_creator': 'yq'
      }
      console.log(data)
      let _this = this
      postAPI('/base/roleAdd', data).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.clearform()
          _this.getData()
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
    },
    // 关闭授权窗口二次确认
    closeRolePower () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.powerVisible = false
        })
        .catch(() => {
          this.powerVisible = true
        })
    },
    // 授权
    handlePower (row) {
      this.powerform = row
      console.log(row)
      let _this = this
      this.$nextTick(() => _this.$refs.RolePower.getForm())
      this.powerVisible = true
    },
    // 保存授权
    savePower () {
      this.$refs.RolePower.save()
    },
    closePower () {
      this.powerVisible = false
      this.getData()
    }
  }
}
</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
  }
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
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
</style>
