<template>
  <div>
    <div v-if=checkshow>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 期初库存
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
        <el-table-column prop="oi_iden" sortable label="单据编号" align="center"></el-table-column>
        <el-table-column prop="oi_orga" sortable label="库存组织" :filters="oi_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="oi_to" sortable label="仓库" :filters="oi_toSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="oi_req_date" sortable label="盘点日期" align="center"></el-table-column>
        <el-table-column prop="oi_status" sortable label="状态" :filters="oi_statusSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.oi_status==='已审批'?'success':''"
            >{{scope.row.oi_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="oi_creator" sortable label="创建人" :filters="oi_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="oi_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.oi_status==='草稿'"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.oi_status==='草稿'"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.oi_status==='已审批'"
            >详情
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
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :deoioy-on-close="true" :before-close="closePcedit">
      <Beginadd ref="Reqedit" :editform="editform" :ifchange="true"></Beginadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :deoioy-on-close="true">
      <Beginadd ref="Reqmore" :editform="moreform" :ifchange="false"></Beginadd>
    </el-dialog>
  </div>
    <!-- 新增弹出框 -->
    <div title="新增" v-if="addVisible" width="90%" :close-on-click-modal="false">
      <el-page-header @back="back" content="新增"></el-page-header>
      <Beginadd ref="Transferadd" @close="close" :editform="addform" :ifchange="true"></Beginadd>
    </div>
  </div>
</template>

<script>
import { postAPI } from '../../../../api/api'
import Beginadd from './BeginAdd'

export default {
  name: 'oi_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      oi_orgaSet: [],
      oi_toSet: [],
      oi_fromSet: [],
      oi_dpmSet: [],
      oi_statusSet: [],
      oi_creatorSet: [],
      editVisible: false,
      checkshow: true,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        oi_iden: '',
        oi_orga: '',
        oi_from: '',
        oi_to: '',
        oi_req_date: ''
      }
    }
  },
  components: {
    Beginadd
  },
  created () {
    // this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/oi_check').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let orgaset = new Set()
        let toset = new Set()
        let dpmset = new Set()
        let statusset = new Set()
        let fromset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['oi_orga'])
          fromset.add(_this.tableData[i]['oi_from'])
          toset.add(_this.tableData[i]['oi_to'])
          dpmset.add(_this.tableData[i]['oi_req_department'])
          statusset.add(_this.tableData[i]['oi_status'])
          creatorset.add(_this.tableData[i]['oi_creator'])
        }
        for (let i of orgaset) {
          _this.oi_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of fromset) {
          _this.oi_fromSet.push({
            text: i,
            value: i
          })
        }
        for (let i of toset) {
          _this.oi_toSet.push({
            text: i,
            value: i
          })
        }
        for (let i of dpmset) {
          _this.oi_dpmSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.oi_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.oi_creatorSet.push({
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
          data.oi_iden.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_orga.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_to.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_from.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_req_department.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_req_date.toLowerCase().includes(this.search.toLowerCase()) ||
          data.oi_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      this.checkshow = false
    },
    // 返回
    back () {
      this.checkshow = true
      this.addVisible = false
    },
    // 关闭新增弹窗
    close () {
      this.addVisible = false
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
          this.find()
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
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 关闭窗口二次确认
    closePcedit () {
      this.$confirm('确定要关闭吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.editVisible = false
        })
        .catch(() => {
          this.editVisible = true
        })
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
