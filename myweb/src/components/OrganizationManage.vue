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
        <el-input v-model="query.name" placeholder="请输入内容" class="handle-input mr10"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
        <el-button type="primary" icon="el-icon-circle-plus-outline" @click="handleAlter" class="alterbutton">新增</el-button>
      </div>
      <el-table
        :data="tableData"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
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
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="alterVisible" width="40%" >
        <el-form ref="form" :model="form" label-width="80px" >
          <el-row>
            <el-form-item label="部门名称"  align="left">
              <el-col :span="10">
                <el-input v-model="form.dpm_name" class="name"></el-input>
              </el-col>
              <el-switch
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
                        placeholder="请输入内容" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="alterVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAlter">确 定</el-button>
            </span>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
      <el-form ref="form" :model="editform" label-width="70px">
        <el-form-item label="部门名称">
          <el-input v-model="editform.dpm_name"></el-input>
        </el-form-item>
        <el-switch
          v-model="editform.dpm_center"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-text="中心"
          inactive-text="其他"
          active-value="1"
          inactive-value="0">
        </el-switch>
      </el-form>
      <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 10
      },
      form: {},
      dpm_name: '',
      dpm_orgaSet: [],
      dpm_creatorSet: [],
      editform: {},
      tableData: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0,
      idx: -1,
      id: -1
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      axios.post('/test2').then(function (res) {
        _this.tableData = res.data.list
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
    find () {
    },
    // 触发搜索按钮
    handleSearch () {
      this.$set(this.query, 'pageIndex', 1)
      this.getData()
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 禁用操作
    handleStop (row) {
      axios.post('/test2', {data: row, status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 启用
    handleStart (row) {
      axios.post('/test2', {data: row, status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform = row
      this.dpm_name = row.dpm_name
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      axios.post('/test2', {data: this.editform, dpm_name: this.dpm_name}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      this.alterVisible = false
      this.$message.success(`新增成功`)
      axios.post('/test2', {data: this.form}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.$set(this.query, 'pageIndex', val)
      this.getData()
    }
  }
}
</script>

<style scoped>
  .handle-box {
    margin-bottom: 20px;
    position: relative;
  }
  .people {
    width:200px;
    position: relative;
  }
  .handle-select {
    width: 120px;
  }

  .handle-input {
    width: 300px;
    display: inline-block;
  }
  .alterbutton{
    position: absolute;
    right:0;
  }
  .handle-del {
    position: absolute;
    right:90px;
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
  .mr10 {
    margin-right: 10px;
  }
</style>
