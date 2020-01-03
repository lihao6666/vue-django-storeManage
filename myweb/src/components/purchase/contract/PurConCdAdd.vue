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
        <el-select v-model="formadd.pc_orga" placeholder="请选择库存组织" :disabled="ifhasorga">
          <el-option v-for="item in form_pc_orga" v-bind:key="item" :label="item" :value="item"></el-option>
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
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{props.row.cd_prd_remarks}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="cd_iden" sortable label="物料编码" :filters="cd_idenSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_name" sortable label="物料名称" :filters="cd_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_specification" sortable label="规格" :filters="cd_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_model" sortable label="型号" :filters="cd_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_meterage" sortable label="单位" :filters="cd_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_prd_num" sortable label="申请数量" align="center"></el-table-column>
        <el-table-column prop="cd_present_num" sortable label="现存量" align="center"></el-table-column>
        <el-table-column prop="cd_rp_iden" sortable label="请购单号" :filters="cd_rp_idenSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_rp_date" sortable label="请购日期" align="center"></el-table-column>
        <el-table-column prop="cd_rp_from" sortable label="申请部门" :filters="cd_rp_fromSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_rp_creator" sortable label="申请人" :filters="cd_rp_creatorSet"
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
  props: ['tableHas', 'formadd', 'ifhasorga'],
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
      cd_idenSet: [],
      cd_nameSet: [],
      cd_specificationSet: [],
      cd_modelSet: [],
      cd_meterageSet: [],
      cd_attrSet: [],
      cd_rp_idenSet: [],
      cd_rp_fromSet: [],
      cd_rp_creatorSet: [],
      pageTotal: 0,
      ifshowadd: true,
      form_pc_orga: [
        '合肥工业大学'
      ]
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      postAPI('/base/pc_cd_add', this.formadd.po_orga).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        let rpidenset = new Set()
        let idenset = new Set()
        let rpfromset = new Set()
        let rpcreatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['cd_name'])
          specificationset.add(_this.tableData[i]['cd_specification'])
          modelset.add(_this.tableData[i]['cd_model'])
          meterageset.add(_this.tableData[i]['cd_meterage'])
          attrset.add(_this.tableData[i]['cd_attr'])
          rpidenset.add(_this.tableData[i]['cd_rp_iden'])
          rpfromset.add(_this.tableData[i]['cd_rp_from'])
          rpcreatorset.add(_this.tableData[i]['cd_rp_creator'])
          idenset.add(_this.tableData[i]['cd_iden'])
        }
        for (let i of nameset) {
          _this.cd_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.cd_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.cd_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.cd_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.cd_attrSet.push({
            text: i,
            value: i
          })
        }
        for (let i of rpidenset) {
          _this.cd_rp_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of idenset) {
          _this.cd_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of rpfromset) {
          _this.cd_rp_fromSet.push({
            text: i,
            value: i
          })
        }
        for (let i of rpcreatorset) {
          _this.cd_rp_creatorSet.push({
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
        String(data.cd_iden).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_name).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_specification).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_model).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_rp_iden).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_rp_from).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_rp_creator).toLowerCase().includes(this.search.toLowerCase()) ||
        String(data.cd_meterage).toLowerCase().includes(this.search.toLowerCase())))
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
        if (this.tableHas[i].cd_iden === row.cd_iden && this.tableHas[i].cd_rp_iden === row.cd_rp_iden) {
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
