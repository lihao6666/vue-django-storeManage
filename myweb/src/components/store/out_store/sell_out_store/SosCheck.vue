<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 销售出库
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
                <span>{{ props.row.sos_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="sos_iden" sortable label="出库单编号" align="center"></el-table-column>
        <el-table-column prop="sos_orga" sortable label="库存组织" :filters="sos_orgaSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sos_warehouse" sortable label="出库仓库" :filters="sos_warehouseSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sos_type" sortable label="出库分类" :filters="sos_typeSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sos_date" sortable label="出库日期" align="center"></el-table-column>
        <el-table-column prop="sos_from_iden" sortable label="来源单据号" align="center"></el-table-column>
        <el-table-column prop="sos_status" sortable label="状态" :filters="sos_statusSet"
      :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.sos_status==='已审批'?'success':''"
            >{{scope.row.sos_status}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sos_creator" sortable label="创建人" :filters="sos_creatorSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sos_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-postcard"
              class="green"
              @click="handleMore(scope.$index, scope.row)"
              v-if="scope.row.sos_status==='已审批'"
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
    <!-- 详情弹出框 -->
    <el-dialog title="详情" :visible.sync="moreVisible" width="90%" :destroy-on-close="true">
      <SosDetail :editform="moreform"></SosDetail>
    </el-dialog>
  </div>
</template>

<script>
import SosDetail from './SosDetail'
import { postAPI } from '../../../../api/api'

export default {
  name: 'sos_check',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      sos_orgaSet: [],
      sos_warehouseSet: [],
      sos_typeSet: [],
      sos_statusSet: [],
      sos_creatorSet: [],
      moreVisible: false,
      moreform: {
        sos_iden: ''
      },
      pageTotal: 0
    }
  },
  components: {
    SosDetail
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/sos_check').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let orgaset = new Set()
        let nameset = new Set()
        let statusset = new Set()
        let typeset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          orgaset.add(_this.tableData[i]['sos_orga'])
          typeset.add(_this.tableData[i]['sos_type'])
          nameset.add(_this.tableData[i]['sos_warehouse'])
          statusset.add(_this.tableData[i]['sos_status'])
          creatorset.add(_this.tableData[i]['sos_creator'])
        }
        for (let i of orgaset) {
          _this.sos_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.sos_typeSet.push({
            text: i,
            value: i
          })
        }
        for (let i of nameset) {
          _this.sos_warehouseSet.push({
            text: i,
            value: i
          })
        }
        for (let i of statusset) {
          _this.sos_statusSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.sos_creatorSet.push({
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
        data.sos_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sos_orga.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sos_warehouse.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sos_type.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sos_creator.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 详情操作
    handleMore (index, row) {
      this.moreform = row.sos_iden
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
