<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料
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
        <el-switch
          v-model="ifshowadd"
          @change="switchChange"
          class="el-switch-ifshowadd"
          active-text="显示已添加">
        </el-switch>
        <el-button type="primary" class="button-save" @click="save">添 加</el-button>
      </div>
      <el-table
        max-height="580"
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
        size="mini"
      >
        <el-table-column type="selection" :selectable="selectable" width="55"></el-table-column>
        <el-table-column prop="sod_iden" sortable label="物料编码" align="center"></el-table-column>
        <el-table-column prop="sod_name" sortable label="物料名称" :filters="sod_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_specification" sortable label="规格" :filters="sod_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_model" sortable label="型号" :filters="sod_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_meterage" sortable label="计量单位" :filters="sod_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_attr" sortable label="存货属性" :filters="sod_attrSet"
      :filter-method="filter" align="center">
        </el-table-column>
        <el-table-column prop="sod_present_num" sortable label="现存量" align="center"></el-table-column>
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
import {postAPI} from '../../api/api'

export default {
  name: 'req_pur_sod',
  props: ['tableHas'],
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
      sod_nameSet: [],
      sod_specificationSet: [],
      sod_modelSet: [],
      sod_meterageSet: [],
      sod_attrSet: [],
      pageTotal: 0,
      ifshowadd: true
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/so_sod_add').then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['sod_name'])
          specificationset.add(_this.tableData[i]['sod_specification'])
          modelset.add(_this.tableData[i]['sod_model'])
          meterageset.add(_this.tableData[i]['sod_meterage'])
          attrset.add(_this.tableData[i]['sod_attr'])
        }
        for (let i of nameset) {
          _this.sod_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.sod_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.sod_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.sod_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.sod_attrSet.push({
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
      this.tableDataNew = this.tableData.filter(data => (this.ifshowadd || this.selectable(data, 0)) &&
        (!this.search ||
        data.sod_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sod_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sod_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sod_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.sod_meterage.toLowerCase().includes(this.search.toLowerCase())))
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 多选操作
    handleSelectionChange (val) {
      this.multipleSelection = val
    },
    // 显示已添加按钮的事件
    switchChange (val) {
      this.find()
    },
    // 可选项
    selectable (row, index) {
      for (let i in this.tableHas) {
        if (this.tableHas[i].sod_iden === row.sod_iden) {
          return false
        }
      }
      return true
    },
    // 保存
    save () {
      this.$emit('add', this.multipleSelection)
      this.multipleSelection = []
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
  .el-switch-ifshowadd {
    margin-left: 30px;
  }
</style>
