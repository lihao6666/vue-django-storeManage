<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 请购单
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
        <el-button type="primary" icon="el-icon-plus" class="button-plus" @click="add">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{ props.row.req_pur_remarks }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭人">
                <span>{{ props.row.req_pur_closer }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭时间">
                <span>{{ props.row.req_pur_closeDate }}</span>
              </el-form-item>
              <el-form-item v-if="props.row.req_pur_status==='已关闭'" label="关闭原因">
                <span>{{ props.row.req_pur_closeReason}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="req_pur_iden" sortable label="请购单号" align="center"></el-table-column>
        <el-table-column prop="req_pur_orga" sortable label="库存组织" :filters="req_pur_orgaSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_type" sortable label="需求类型" :filters="req_pur_typeSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_from" sortable label="申请部门" :filters="req_pur_fromSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_date" sortable label="请购日期" align="center"></el-table-column>
        <el-table-column prop="req_pur_status" sortable label="状态" :filters="req_pur_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top" v-if="scope.row.req_pur_status==='已关闭'">
              <p>关闭人: {{ scope.row.req_pur_closer }}</p>
              <p>关闭时间: {{ scope.row.req_pur_closeDate }}</p>
              <p>关闭原因: {{ scope.row.req_pur_closeReason }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag :type="'info'">{{scope.row.req_pur_status}}</el-tag>
              </div>
            </el-popover>
            <el-tag v-else
              :type="scope.row.req_pur_status==='已审批'?'success':(scope.row.req_pur_status==='已关闭'?'info':'')"
            >{{scope.row.req_pur_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="req_pur_creator" sortable label="创建人" :filters="req_pur_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="req_pur_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='草稿'"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='草稿'"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='已审批' || scope.row.req_pur_status==='已关闭'"
            >详情
            </el-button>
            <el-button
              type="text"
              icon="el-icon-document-delete"
              class="block"
              @click="handleClose(scope.$index, scope.row)"
              v-if="scope.row.req_pur_status==='已审批'"
            >关闭
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
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
    <el-dialog title="新增" :visible.sync="addVisible" width="90%">
      <Reqadd ref="Reqadd" :editform="addform" :ifchange="true"></Reqadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%">
      <Reqadd ref="Reqedit" :editform="editform" :ifchange="true"></Reqadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%">
      <Reqadd ref="Reqmore" :editform="moreform" :ifchange="false"></Reqadd>
    </el-dialog>
  </div>
</template>

<script>
import Reqadd from './req_pur_add'
import { postAPI, getAPI } from '../../api/api'

export default {
  name: 'req_pur_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      req_pur_orgaSet: [],
      req_pur_typeSet: [],
      req_pur_fromSet: [],
      req_pur_statusSet: [],
      req_pur_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        req_pur_orga: '',
        req_pur_from: '',
        req_pur_type: '',
        req_pur_remarks: '',
        req_pur_date: ''
      }
    }
  },
  components: {
    Reqadd
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      console.log(postAPI('/req_pur_check'))
      console.log(getAPI('/req_pur_check'))
      postAPI('/req_pur_check').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let orgaset = new Set()
        let typeset = new Set()
        let statusset = new Set()
        let fromset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['req_pur_orga'])
          fromset.add(_this.tableData[i]['req_pur_from'])
          typeset.add(_this.tableData[i]['req_pur_type'])
          statusset.add(_this.tableData[i]['req_pur_status'])
          creatorset.add(_this.tableData[i]['req_pur_creator'])
        }
        for (let i of orgaset) {
          _this.req_pur_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of fromset) {
          _this.req_pur_fromSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.req_pur_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.req_pur_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.req_pur_creatorSet.push({
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
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        data.req_pur_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.req_pur_orga.toLowerCase().includes(this.search.toLowerCase()) ||
        data.req_pur_type.toLowerCase().includes(this.search.toLowerCase()) ||
        data.req_pur_from.toLowerCase().includes(this.search.toLowerCase()) ||
        data.req_pur_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.$message.success('删除成功')
          this.tableData.splice(index, 1)
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    // 编辑操作
    handleEdit (index, row) {
      this.editform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Reqedit.getForm())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Reqmore.getForm())
      this.moreVisible = true
    },
    // 关闭操作
    handleClose (index, row) {
      this.$prompt('请输入关闭原因', '关闭', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(({ value }) => {
        this.$confirm('确定要关闭吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.$message.success('关闭成功')
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消关闭'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消关闭'
        })
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
  }

  .table {
    width: 100%;
    font-size: 14px;
  }

  .red {
    color: #ff0000;
  }

  .green {
    color: #00a854;
  }

  .block {
    color: grey;
  }

  .input-search {
    width: 50%;
  }
  .button-plus {
    float: right;
  }
</style>
