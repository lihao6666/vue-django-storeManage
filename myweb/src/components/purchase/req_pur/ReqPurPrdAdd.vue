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
        <el-select v-model="formadd.orga_name" placeholder="请选择库存组织" :disabled="ifhasorga" @change="changeOrga">
          <el-option v-for="item in orga_name" v-bind:key="item" :label="item" :value="item"></el-option>
        </el-select>
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
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
        size="mini"
      >
        <el-table-column type="selection" :selectable="selectable" width="55"></el-table-column>
        <el-table-column prop="material_iden" sortable label="物料编码" align="center"></el-table-column>
        <el-table-column prop="material_name" sortable label="物料名称" :filters="material_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_specification" sortable label="规格" :filters="material_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_model" sortable label="型号" :filters="material_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="meterage_name" sortable label="计量单位" :filters="meterage_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_attr" sortable label="存货属性" :filters="material_attrSet"
      :filter-method="filter" align="center">
        </el-table-column>
        <el-table-column prop="prd_present_num" sortable label="现存量" align="center"></el-table-column>
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
  name: 'pr_prd',
  props: ['tableHas', 'formadd', 'ifhasorga', 'orga_name'],
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
      material_nameSet: [],
      material_specificationSet: [],
      material_modelSet: [],
      meterage_nameSet: [],
      material_attrSet: [],
      pageTotal: 0,
      ifshowadd: true
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      if (this.formadd.orga_name === '') {
        return
      }
      let _this = this
      postAPI('/purchaseRequest/prdNew', {'orga_name': _this.formadd.orga_name}).then(function (res) {
        console.log(res.data)
        _this.tableData = res.data.materials
        for (let i in _this.tableData) {
          _this.tableData[i].prd_num = 1
          _this.tableData[i].prd_present_num = res.data.prds_present_num[i]
          _this.tableData[i].prd_iden = _this.tableData[i].material_iden
          _this.tableData[i].prd_name = _this.tableData[i].material_name
          _this.tableData[i].prd_specification = _this.tableData[i].material_specification
          _this.tableData[i].prd_model = _this.tableData[i].material_model
          _this.tableData[i].prd_meterage = _this.tableData[i].meterage_name
          _this.tableData[i].prd_remarks = ''
        }
        console.log(_this.tableData)
        _this.pageTotal = res.data.materials.length
        _this.find()
        _this.material_nameSet = []
        _this.material_specificationSet = []
        _this.material_modelSet = []
        _this.meterage_nameSet = []
        _this.material_attrSet = []
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['material_name'])
          specificationset.add(_this.tableData[i]['material_specification'])
          modelset.add(_this.tableData[i]['material_model'])
          meterageset.add(_this.tableData[i]['meterage_name'])
          attrset.add(_this.tableData[i]['material_attr'])
        }
        for (let i of nameset) {
          _this.material_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.meterage_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.material_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.material_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.material_attrSet.push({
            text: i,
            value: i
          })
        }
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
        data.material_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.material_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.material_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.material_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.meterage_name.toLowerCase().includes(this.search.toLowerCase())))
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
        if (this.tableHas[i].prd_iden === row.material_iden) {
          return false
        }
      }
      return true
    },
    // 保存
    save () {
      this.$emit('add', this.multipleSelection)
      this.multipleSelection = []
      this.$refs.multipleTable.clearSelection()
    },
    // 选择组织
    changeOrga () {
      console.log(this.formadd.orga_name)
      this.getData()
    }
  }
}
</script>

<style>
  .tableRowDisplay {
    display: none;
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
    width: 40%;
  }
  .button-save {
    float: right;
    margin-left: 30px;
  }
  .el-switch-ifshowadd {
    margin-left: 30px;
  }
</style>
