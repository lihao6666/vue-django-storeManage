<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 组织架构管理
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
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.dpm_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="dpm_name" sortable label="部门名称" :filters="dpm_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="dpm_center" sortable label="是否中心" :filters="dpm_centerSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.dpm_center===1?'success':''">{{centortype[scope.row.dpm_center].label}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="dpm_creator" sortable label="创建人" :filters="dpm_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="dpm_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.dpm_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.dpm_status===0"
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="40%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="80px" >
          <el-row>
            <el-form-item label="部门名称"  align="left">
              <el-col :span="10">
                <el-input v-model="form.dpm_name" class="name"></el-input>
              </el-col>
              <el-switch
                class="el-switch-center"
                v-model="form.dpm_center"
                active-color="#13ce66"
                inactive-color="#0074D9"
                active-text="中心"
                inactive-text="非中心部门"
                :active-value="centortype[1].value"
                :inactive-value="centortype[0].value">
              </el-switch>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.dpm_remarks"
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
          <el-button type="primary" @click="saveAlter" >确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="40%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="80px" >
          <el-row>
            <el-form-item label="部门名称"  align="left">
              <el-col :span="10">
                <el-input v-model="editform.dpm_name" class="name"></el-input>
              </el-col>
              <el-switch
                v-model="editform.dpm_center"
                disabled
                class="el-switch-center"
                active-color="#13ce66"
                inactive-color="#0074D9"
                active-text="中心"
                inactive-text="非中心部门"
                :active-value="centortype[1].value"
                :inactive-value="centortype[0].value">
              </el-switch>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.dpm_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
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
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'OrganizationManage',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      centortype: [
        {
          value: 0,
          label: '非中心部门'
        },
        {
          value: 1,
          label: '中心'
        }
      ],
      search: '',
      form: {
        dpm_name: '',
        dpm_center: 0,
        dpm_remarks: ''
      },
      dpm_name: '',
      dpm_orgaSet: [],
      dpm_centerSet: [],
      dpm_creatorSet: [],
      editform: {
        dpm_name: '',
        dpm_center: 0,
        dpm_remarks: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
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
      let _this = this
      getAPI('/base/departments').then(function (res) {
        console.log(res.data)
        _this.tableData = res.data.departments
        _this.pageTotal = res.data.departments.length
        _this.dpm_orgaSet = []
        _this.dpm_centerSet = []
        _this.dpm_creatorSet = []
        _this.find()
        let orgaset = new Set()
        let centerset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['dpm_name'])
          creatorset.add(_this.tableData[i]['dpm_creator'])
          centerset.add(_this.tableData[i]['dpm_center'])
        }
        for (let i of centerset) {
          _this.dpm_centerSet.push({
            text: _this.centortype[i].label,
            value: i
          })
        }
        for (let i of orgaset) {
          _this.dpm_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.dpm_creatorSet.push({
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
    // 一键清除新增表单
    clearform () {
      this.form.dpm_name = ''
      this.form.dpm_center = 0
      this.form.dpm_remarks = ''
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          row.dpm_status = 0
          console.log(row)
          let _this = this
          postAPI('/base/departmentStatus', row).then(function (res) {
            console.log(res.data)
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.dpm_status = 1
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.dpm_status = 1
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        String(data.dpm_name).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.dpm_center).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.dpm_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.dpm_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.dpm_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          row.dpm_status = 1
          let _this = this
          postAPI('/base/departmentStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.dpm_status = 0
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.dpm_status = 0
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
      this.editform.dpm_name = row.dpm_name
      this.editform.dpm_center = row.dpm_center
      this.editform.dpm_remarks = row.dpm_remarks
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      console.log(this.editform)
      if (!this.editform.dpm_name) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/departmentUpdate', this.editform).then(function (res) {
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
      if (!this.form.dpm_name) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/departmentAdd', this.form).then(function (res) {
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
      console.log(val)
    },
    handleSizeChange (val) {
      this.query.pageSize = val
      console.log(val)
    }
  }
}
</script>

<style>
  .el-switch-center {
    margin-left: 30px;
  }
  .el-row-button-save {
    top: 15px;
  }
  .tableRowDisplay {
    display: none;
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
  .l {
    color: #0074D9;
  }
</style>
