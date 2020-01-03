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
        <el-button
          type="primary"
          icon="el-icon-delete"
          @click="delAllSelection"
          v-if="ifchange"
        >批量删除</el-button>
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" class="button-save" v-if="ifchange">保 存</el-button>
        <el-button type="primary" class="button-save" v-if="ifchange" :disabled="!tableDataNew.length>0">提 交</el-button>
        <el-button type="primary" icon="el-icon-plus" class="button-save" @click="add" v-if="ifchange">新增</el-button>
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
        <el-table-column
          type="selection"
          v-if="ifchange"
          width="55">
        </el-table-column>
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注">
                <el-input type="textarea" v-model="props.row.prd_remarks" rows="3" :disabled="!ifchange"
                    placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="prd_iden" sortable label="物料编码" align="center"></el-table-column>
        <el-table-column prop="prd_name" sortable label="物料名称" :filters="prd_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="prd_specification" sortable label="规格" :filters="prd_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="prd_model" sortable label="型号" :filters="prd_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="prd_meterage" sortable label="单位" :filters="prd_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="prd_num" sortable label="请购数量" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.prd_num"
              @input="scope.row.prd_num = inputnum(scope.row.prd_num)"
              @change="scope.row.prd_num = changenum(scope.row.prd_num)"
              clearable>
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="prd_present_num" sortable label="现存量" align="center"></el-table-column>
        <el-table-column label="操作" align="center" v-if="ifchange">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
            >删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          ref="pagination"
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
    <el-dialog title="新增物料" :visible.sync="addVisible" width="90%" append-to-body>
      <Prdadd @add="addPrd" :tableHas="tableData" :formadd="formadd" :ifhasorga="ifhasorga"></Prdadd>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI} from '../../api/api'
import Prdadd from './ReqPurPrdAdd'

export default {
  name: 'req_pur_prd',
  props: ['formadd', 'ifchange'],
  components: {
    Prdadd
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
      prd_nameSet: [],
      prd_specificationSet: [],
      prd_modelSet: [],
      prd_meterageSet: [],
      addVisible: false,
      pageTotal: 0,
      ifhasorga: false
    }
  },
  created () {
    this.getData()
    this.$nextTick(function () {
      if (!this.formadd.req_pur_orga) {
        this.addVisible = true
      }
    })
  },
  methods: {
    getData () {
      if (this.formadd.req_pur_iden === '') {
        return
      }
      let _this = this
      postAPI('/req_pur_prd', this.formadd).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['prd_name'])
          specificationset.add(_this.tableData[i]['prd_specification'])
          modelset.add(_this.tableData[i]['prd_model'])
          meterageset.add(_this.tableData[i]['prd_meterage'])
        }
        for (let i of nameset) {
          _this.prd_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.prd_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.prd_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.prd_modelSet.push({
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
        data.prd_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.prd_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.prd_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.prd_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.prd_meterage.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      if (this.formadd.req_pur_orga === '') {
        this.ifhasorga = false
      } else {
        this.ifhasorga = true
      }
    },
    // 新增物料
    addPrd (val) {
      for (let i in val) {
        val[i].prd_num = 1
      }
      this.tableData = this.tableData.concat(val)
      this.find()
      let message = '新增' + val.length + '条'
      this.$message.success(message)
      this.addVisible = false
    },
    // 修改数量
    inputnum (num) {
      num = num.replace(/[^\d]/g, '')
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      return num
    },
    changenum (num) {
      if (num < 1) {
        num = 1
      }
      return num
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
    // 批量删除
    delAllSelection () {
      let delnum = this.multipleSelection.length
      if (delnum === 0) {
        return
      }
      this.$confirm('确定要删除' + delnum + '条吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let pageIndexNew = Math.ceil((this.pageTotal - this.multipleSelection.length) / this.query.pageSize) // 新的页面数量
          this.query.pageIndex = (this.query.pageIndex > pageIndexNew) ? pageIndexNew : this.query.pageIndex
          this.query.pageIndex = (this.query.pageIndex === 0) ? 1 : this.query.pageIndex
          for (let i in this.multipleSelection) {
            let x = this.tableData.valueOf(this.multipleSelection[i])
            this.tableData.splice(x, 1)
          }
          this.find()
          this.$message.success('删除' + delnum + '条成功')
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
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
  .input-search {
    margin-left: 20px;
    width: 40%;
  }
  .button-save {
    float: right;
    margin-left: 30px;
  }
</style>
