<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料类别维护
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
        max-height="580"
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="type_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="type_name" sortable label="名称" :filters="type_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="type_creator" sortable label="创建人" :filters="type_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="type_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.type_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.type_status==='停用'"
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" >
      <div class="container">
        <el-form ref="form" :model="form" label-width="70px"  class="form" >
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.type_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.type_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="70px">
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.type_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.type_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
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
        type_iden: '',
        type_name: '',
        type_remarks: '',
        type_area: ''
      },
      type_iden: '',
      type_nameSet: [],
      type_creatorSet: [],
      editform: {
        type_iden: '',
        type_name: '',
        type_remarks: '',
        type_area: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
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
      postAPI('/material_type').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let nameset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['type_name'])
          creatorset.add(_this.tableData[i]['type_creator'])
        }
        for (let i of nameset) {
          _this.type_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.type_creatorSet.push({
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
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 一键清除新增表单
    clearform () {
      this.form.type_iden = ''
      this.form.type_iden = ''
      this.form.type_name = ''
      this.form.type_remarks = ''
    },
    // 禁用操作
    handleStop (row) {
      postAPI('/material_type', {data: row, type_status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.type_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      postAPI('/material_type', {data: row, type_status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.type_iden = row.type_iden
      this.editform.type_name = row.type_name
      this.editform.type_remarks = row.type_remarks
      this.type_iden = row.type_iden
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/material_type', {data: this.editform, type_name: this.type_name}).then(function (res) {
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
      postAPI('/material_type', {data: this.form, table: 'material_type'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
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
}</script>

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
  .inputs {
    width: 590px;
  }
</style>
