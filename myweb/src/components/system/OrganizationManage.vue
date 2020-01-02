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
        <el-table-column prop="dpm_center" sortable label="是否中心" align="center"></el-table-column>
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
              v-if="scope.row.dpm_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.dpm_status==='停用'"
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="40%" >
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
                inactive-color="#ff4949"
                active-text="中心"
                inactive-text="其他"
                active-value="1"
                inactive-value="0">
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
    <el-dialog title="编辑" :visible.sync="editVisible" width="40%">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="80px" >
          <el-row>
            <el-form-item label="部门名称"  align="left">
              <el-col :span="10">
                <el-input v-model="editform.dpm_name" class="name"></el-input>
              </el-col>
              <el-switch
                v-model="editform.dpm_center"
                class="el-switch-center"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="中心"
                inactive-text="其他"
                active-value="1"
                inactive-value="0">
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
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="3">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        dpm_name: '',
        dpm_center: '',
        dpm_remarks: ''
      },
      dpm_name: '',
      dpm_orgaSet: [],
      dpm_creatorSet: [],
      editform: {
        dpm_name: '',
        dpm_center: '',
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
      postAPI('/department').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let orgaset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['dpm_name'])
          creatorset.add(_this.tableData[i]['dpm_creator'])
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
        _this.pageTotal = res.data.list.length
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
      this.form.dpm_center = ''
      this.form.dpm_remarks = ''
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 禁用操作
    handleStop (row) {
      postAPI('/department', {data: row, status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
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
      postAPI('/department', {data: row, status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.dpm_name = row.dpm_name
      this.editform.dpm_center = row.dpm_center
      this.editform.dpm_remarks = row.dpm_remarks
      this.dpm_name = row.dpm_name
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/department', {data: this.editform, dpm_name: this.dpm_name}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      this.alterVisible = false
      this.$message.success(`新增成功`)
      this.clearform()
      postAPI('/department', {data: this.form, table: 'department'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
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
</style>
