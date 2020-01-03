<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 采购订单
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
        <el-button type="primary" icon="el-icon-plus" class="button-plus" @click="addpc">按采购合同</el-button>
        <el-button type="primary" icon="el-icon-plus" class="button-plus" @click="addrp">按请购单</el-button>
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
                <span>{{ props.row.po_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="po_iden" sortable label="订单编号" align="center"></el-table-column>
        <el-table-column prop="po_orga" sortable label="库存组织" :filters="po_orgaSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_supply" sortable label="供应商" :filters="po_supplySet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_date" sortable label="订单日期" align="center"></el-table-column>
        <el-table-column prop="po_sum" sortable label="价税合计" align="center"></el-table-column>
        <el-table-column prop="po_contractFrom" sortable label="来源合同" :filters="po_contractFromSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_status" sortable label="状态" :filters="po_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.po_status==='已审批'?'success':''"
            >{{scope.row.po_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="po_creator" sortable label="创建人" :filters="po_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="po_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index, scope.row)"
              v-if="scope.row.po_status==='草稿'"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              v-if="scope.row.po_status==='草稿'"
            >删除
            </el-button>
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.po_status==='已审批'"
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
    <!-- 按请购单弹出框 -->
    <el-dialog title="新增" :visible.sync="addrpVisible" width="90%" :close-on-click-modal="false">
      <Poadd ref="poaddrp" :editform="addrpform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 按采购合同弹出框 -->
    <el-dialog title="新增" :visible.sync="addpcVisible" width="90%" :close-on-click-modal="false">
      <Poadd ref="poaddpc" :editform="addpcform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="90%" :close-on-click-modal="false" :destroy-on-close="true" :before-close="closepoedit">
      <Poadd ref="poedit" :editform="editform" :ifchange="true"></Poadd>
    </el-dialog>
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <Poadd ref="pomore" :editform="moreform" :ifchange="false"></Poadd>
    </el-dialog>
  </div>
</template>

<script>
import Poadd from './PurOrdAdd'
import { postAPI } from '../../../api/api'

export default {
  name: 'po_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      po_orgaSet: [],
      po_contractFromSet: [],
      po_supplySet: [],
      po_statusSet: [],
      po_creatorSet: [],
      editVisible: false,
      editform: {},
      moreVisible: false,
      moreform: {},
      pageTotal: 0,
      addrpVisible: false,
      addpcVisible: false,
      addrpform: {
        po_iden: '',
        po_orga: '',
        po_supply: '',
        po_contractFrom: '',
        po_remarks: '',
        po_date: '',
        po_sum: 0
      },
      addpcform: {
        po_iden: '',
        po_orga: '',
        po_supply: '',
        po_contractFrom: '1',
        po_remarks: '',
        po_date: '',
        po_sum: 0
      }
    }
  },
  components: {
    Poadd
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/base/po_check').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let orgaset = new Set()
        let nameset = new Set()
        let statusset = new Set()
        let supplyset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['po_orga'])
          supplyset.add(_this.tableData[i]['po_supply'])
          nameset.add(_this.tableData[i]['po_contractFrom'])
          statusset.add(_this.tableData[i]['po_status'])
          creatorset.add(_this.tableData[i]['po_creator'])
        }
        for (let i of orgaset) {
          _this.po_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of supplyset) {
          _this.po_supplySet.push({
            text: i,
            value: i
          })
        }
        for (let i of nameset) {
          _this.po_contractFromSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.po_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.po_creatorSet.push({
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
        data.po_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.po_orga.toLowerCase().includes(this.search.toLowerCase()) ||
        data.po_contractFrom.toLowerCase().includes(this.search.toLowerCase()) ||
        data.po_supply.toLowerCase().includes(this.search.toLowerCase()) ||
        data.po_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    addrp () {
      this.addrpVisible = true
    },
    addpc () {
      this.addpcVisible = true
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
      this.$nextTick(() => _this.$refs.poedit.getForm())
      this.editVisible = true
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row
      let _this = this
      this.$nextTick(() => _this.$refs.pomore.getForm())
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
    },
    // 关闭窗口二次确认
    closepoedit () {
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
    margin-left: 30px;
  }
</style>
