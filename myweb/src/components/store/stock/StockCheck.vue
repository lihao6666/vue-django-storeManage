<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 现存量查询
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <row>
          <el-input
            placeholder="关键字搜索"
            prefix-icon="el-icon-search"
            class="input-search"
            @input="find"
            clearable
            v-model="search">
          </el-input>
        </row>
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
        <el-table-column prop="orga_name" sortable label="库存组织" :filters="stock_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="warehouse" sortable label="仓库" :filters="stock_wareSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_iden" sortable label="物料编码"  align="center"></el-table-column>
        <el-table-column prop="material_name" sortable label="物料名称" :filters="stock_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_specification" sortable label="规格" :filters="stock_specSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_model" sortable label="型号" :filters="stock_modelSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_meterage" sortable label="单位" :filters="stock_meterageSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="present_num" sortable label="现存量" align="center"></el-table-column>
        <el-table-column prop="present_price" sortable label="库存单价"  align="center"></el-table-column>
        <el-table-column prop="present_sum" sortable label="库存金额" align="center"></el-table-column>
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
  </div>
</template>

<script>
import {postAPI} from '../../../api/api'
export default {
  name: 'test',
  data () {
    return {
      orga_options: [],
      center_options: [],
      brand_options: [],
      query: {
        pageIndex: 1,
        pageSize: 10
      },
      search: '',
      center_wh_iden: '',
      stock_orgaSet: [],
      stock_wareSet: [],
      stock_nameSet: [],
      stock_specSet: [],
      stock_modelSet: [],
      stock_meterageSet: [],
      tableData: [],
      tableDataNew: [],
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
      postAPI('/stock_check').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let orgaSet = new Set()
        let wareSet = new Set()
        let nameSet = new Set()
        let specSet = new Set()
        let modelSet = new Set()
        let meterageSet = new Set()
        for (let i in _this.tableData) {
          orgaSet.add(_this.tableData[i]['orga_name'])
          wareSet.add(_this.tableData[i]['warehouse'])
          nameSet.add(_this.tableData[i]['material_name'])
          specSet.add(_this.tableData[i]['material_specification'])
          modelSet.add(_this.tableData[i]['material_model'])
          meterageSet.add(_this.tableData[i]['material_meterage'])
        }
        for (let i of orgaSet) {
          _this.stock_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of wareSet) {
          _this.stock_wareSet.push({
            text: i,
            value: i
          })
        }
        for (let i of nameSet) {
          _this.stock_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specSet) {
          _this.stock_specSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelSet) {
          _this.stock_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageSet) {
          _this.stock_meterageSet.push({
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
          String(data.material_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_specification).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_model).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.warehouse).toLowerCase().includes(this.search.toLowerCase()))
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
    position: relative;
  }
  .table {
    width: 100%;
    font-size: 14px;
  }
  .input-search {
    width: 50%;
  }
</style>
