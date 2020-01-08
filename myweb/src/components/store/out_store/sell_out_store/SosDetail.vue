<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料明细
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
        @selection-change="handleSelectionChange"
        size="mini"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.sd_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="sd_iden" sortable label="物料编码" :filters="sd_idenSet"
      :filter-method="filter"  align="center"></el-table-column>
        <el-table-column prop="sd_name" sortable label="物料名称" :filters="sd_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sd_specification" sortable label="规格" :filters="sd_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sd_model" sortable label="型号" :filters="sd_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sd_meterage" sortable label="单位" :filters="sd_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sd_num" sortable label="数量" align="center"></el-table-column>
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
  </div>
</template>

<script>
import { postAPI } from '../../../../api/api'

export default {
  name: 'sos_bd',
  props: ['editform'],
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      sd_idenSet: [],
      sd_nameSet: [],
      sd_specificationSet: [],
      sd_modelSet: [],
      sd_meterageSet: [],
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      if (this.editform === '') {
        return
      }
      let _this = this
      postAPI('/sos_bd', this.editform).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let idenset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['sd_name'])
          specificationset.add(_this.tableData[i]['sd_specification'])
          modelset.add(_this.tableData[i]['sd_model'])
          meterageset.add(_this.tableData[i]['sd_meterage'])
          idenset.add(_this.tableData[i]['sd_iden'])
        }
        for (let i of nameset) {
          _this.sd_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of idenset) {
          _this.sd_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.sd_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.sd_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.sd_modelSet.push({
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
        data.sd_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sd_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sd_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sd_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sd_meterage.toLowerCase().includes(this.search.toLowerCase()))
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
  .input-search {
    margin-left: 20px;
    width: 40%;
  }
  .button-save {
    float: right;
    margin-left: 30px;
  }
</style>
