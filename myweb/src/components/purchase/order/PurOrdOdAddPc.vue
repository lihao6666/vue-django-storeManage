<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 采购合同
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-select v-model="formadd.po_orga" placeholder="请选择库存组织" :disabled="ifhasorga" @change="changeSelect">
          <el-option v-for="item in form_po_orga" v-bind:key="item" :label="item" :value="item"></el-option>
        </el-select>
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
        highlight-current-row
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        @current-change="handleCurrentChange"
        size="mini"
      >
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <span>{{props.row.pc_remarks}}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="pc_iden" sortable label="合同编号" align="center"></el-table-column>
        <el-table-column prop="pc_name" sortable label="合同名称" :filters="pc_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pc_supply" sortable label="供应商" :filters="pc_supplySet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="pc_date" sortable label="签订日期" align="center"></el-table-column>
        <el-table-column prop="pc_sum" sortable label="合同金额" align="center"></el-table-column>
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
    <Pcod @add="save"></Pcod>
  </div>
</template>

<script>
import {postAPI} from '../../../api/api'
import Pcod from './PurOrdOdAddPcOd'

export default {
  name: 'pc_cd_add',
  props: ['tableHas', 'formadd', 'ifhasorga'],
  components: {
    Pcod
  },
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
      pc_nameSet: [],
      pc_supplySet: [],
      pageTotal: 0,
      form_po_orga: [
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
      postAPI('/po_od_add_pc', this.formadd.po_orga).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let supplyset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['pc_name'])
          supplyset.add(_this.tableData[i]['pc_supply'])
        }
        for (let i of nameset) {
          _this.pc_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of supplyset) {
          _this.pc_supplySet.push({
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
        data.pc_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pc_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.pc_supply.toLowerCase().includes(this.search.toLowerCase())))
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 单选操作
    handleCurrentChange (val) {
      this.multipleSelection = val
    },
    // 保存
    save (val) {
      this.$emit('add', val)
    },
    // 选择组织
    changeSelect (val) {
      console.log(val)
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
