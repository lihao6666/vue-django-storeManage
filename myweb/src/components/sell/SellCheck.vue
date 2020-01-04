<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 销售订单
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
        <el-table-column prop="so_iden" sortable label="销售订单号" align="center"></el-table-column>
        <el-table-column prop="so_orga" sortable label="库存组织" :filters="so_orgaSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="so_type" sortable label="订单类型" :filters="so_typeSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="so_custom" sortable label="客户" :filters="so_customSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="so_warehouse" sortable label="发货仓库" :filters="so_warehouseSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="so_date" sortable label="订单日期" align="center"></el-table-column>
        <el-table-column prop="so_status" sortable label="状态" :filters="so_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.so_status==='已审批'?'success':''"
            >{{scope.row.so_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="so_creator" sortable label="创建人" :filters="so_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="so_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.so_status==='草稿'"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.so_status==='草稿'"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.so_status==='已审批'"
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
    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="addVisible" width="90%" :close-on-click-modal="false">
      <Soadd ref="Soadd" :editform="addform" :ifchange="true"></Soadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closePcedit">
      <Soadd ref="Soedit" :editform="editform" :ifchange="true"></Soadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <Soadd ref="Somore" :editform="moreform" :ifchange="false"></Soadd>
    </el-dialog>
  </div>
</template>

<script>
import Soadd from './SellAdd'
import {postAPI} from '../../api/api'

export default {
  name: 'sell_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      so_orgaSet: [],
      so_typeSet: [],
      so_customSet: [],
      so_warehouseSet: [],
      so_statusSet: [],
      so_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addVisible: false,
      addform: {
        so_iden: '',
        so_orga: '',
        so_custom: '',
        so_warehouse: '',
        so_type: '',
        so_remarks: '',
        so_date: ''
      }
    }
  },
  components: {
    Soadd
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/so_check').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let orgaset = new Set()
        let typeset = new Set()
        let statusset = new Set()
        let customset = new Set()
        let warehouseset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['so_orga'])
          customset.add(_this.tableData[i]['so_custom'])
          warehouseset.add(_this.tableData[i]['so_warehouse'])
          typeset.add(_this.tableData[i]['so_type'])
          statusset.add(_this.tableData[i]['so_status'])
          creatorset.add(_this.tableData[i]['so_creator'])
        }
        for (let i of orgaset) {
          _this.so_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of customset) {
          _this.so_customSet.push({
            text: i,
            value: i
          })
        }
        for (let i of warehouseset) {
          _this.so_warehouseSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.so_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.so_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.so_creatorSet.push({
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
        data.so_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.so_orga.toLowerCase().includes(this.search.toLowerCase()) ||
        data.so_type.toLowerCase().includes(this.search.toLowerCase()) ||
        data.so_custom.toLowerCase().includes(this.search.toLowerCase()) ||
        data.so_warehouse.toLowerCase().includes(this.search.toLowerCase()) ||
        data.so_creator.toLowerCase().includes(this.search.toLowerCase()))
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
          let pageIndexNew = Math.ceil((this.pageTotal - 1) / this.query.pageSize) // 新的页面数量
          this.query.pageIndex = (this.query.pageIndex > pageIndexNew) ? pageIndexNew : this.query.pageIndex
          this.query.pageIndex = (this.query.pageIndex === 0) ? 1 : this.query.pageIndex
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
      this.$nextTick(() => _this.$refs.Soedit.getForm())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.Somore.getForm())
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
  .input-search {
    width: 50%;
  }
  .button-plus {
    float: right;
  }
</style>
