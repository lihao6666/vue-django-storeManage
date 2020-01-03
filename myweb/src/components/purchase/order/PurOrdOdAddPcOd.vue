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
        <el-button type="primary" class="button-save" @click="save">添 加</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        size="mini"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{props.row.od_rp_remarks}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="od_iden" sortable label="物料编码" :filters="od_idenSet"
      :filter-method="filter"  align="center"></el-table-column>
        <el-table-column prop="od_name" sortable label="物料名称" :filters="od_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="od_specification" sortable label="规格" :filters="od_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="od_model" sortable label="型号" :filters="od_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="od_meterage" sortable label="单位" :filters="od_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="od_num" sortable label="数量" align="center"></el-table-column>
        <el-table-column prop="od_taxRate" sortable label="税率" align="center"></el-table-column>
        <el-table-column prop="od_tax_unitPrice" sortable label="含税单价" align="center"></el-table-column>
        <el-table-column prop="od_unitPrice" sortable label="无税单价" align="center"></el-table-column>
        <el-table-column prop="od_tax_sum" sortable label="含税金额" align="center"></el-table-column>
        <el-table-column prop="od_sum" sortable label="无税金额" align="center"></el-table-column>
        <el-table-column prop="od_tax_price" sortable label="税额" align="center"></el-table-column>
        <el-table-column prop="od_rp_iden" sortable label="请购单号" :filters="od_rp_idenSet"
      :filter-method="filter" align="center"></el-table-column>
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
import {postAPI} from '../../../api/api'

export default {
  name: 'pc_cd_add',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      od_idenSet: [],
      od_nameSet: [],
      od_specificationSet: [],
      od_modelSet: [],
      od_meterageSet: [],
      od_rp_idenSet: [],
      od_attrSet: [],
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/po_od_add_rp').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        let rpidenset = new Set()
        let idenset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['od_name'])
          specificationset.add(_this.tableData[i]['od_specification'])
          modelset.add(_this.tableData[i]['od_model'])
          meterageset.add(_this.tableData[i]['od_meterage'])
          attrset.add(_this.tableData[i]['od_attr'])
          rpidenset.add(_this.tableData[i]['od_rp_iden'])
          idenset.add(_this.tableData[i]['od_iden'])
        }
        for (let i of nameset) {
          _this.od_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.od_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.od_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.od_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of rpidenset) {
          _this.od_rp_idenset.push({
            text: i,
            value: i
          })
        }
        for (let i of idenset) {
          _this.od_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.od_attrSet.push({
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
      this.tableDataNew = this.tableData.filter(data => (!this.search ||
        data.od_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.od_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.od_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.od_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.od_rp_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.od_meterage.toLowerCase().includes(this.search.toLowerCase())))
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 保存
    save () {
      this.$emit('add', this.tableData)
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

  .input-search {
    width: 50%;
  }
  .button-save {
    float: right;
    margin-left: 30px;
  }
</style>
