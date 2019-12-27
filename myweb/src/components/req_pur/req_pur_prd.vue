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
          class="input_search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" class="button_save">保 存</el-button>
        <el-button type="primary" class="button_save">提 交</el-button>
        <el-button type="primary" icon="el-icon-plus" class="button_save" @click="add">新增</el-button>
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
                <span>{{ props.row.prd_remarks }}</span>
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
          @current-change="handlePageChange"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          background
          layout="total, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </div>
    </div>
    <!-- 新增弹出框 -->
    <el-dialog title="新增物料" :visible.sync="addVisible" width="90%" append-to-body>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'req_pur_prd',
  props: ['formadd', 'ifchange'],
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      req_pur: {
        select: '',
        value: ''
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      prd_nameSet: [],
      prd_specificationSet: [],
      prd_modelSet: [],
      prd_meterageSet: [],
      addVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      axios.post('/req_pur_prd', this.req_pur, this.formadd).then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
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
    },
    // 修改数量
    inputnum (num) {
      num = num.replace(/[^\d]/g, '')
      if (!num) {
        num = ''
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
      this.idx = index
      this.form = row
      this.editVisible = true
    },
    handleMore (index, row) {
    },
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
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改第 ${this.idx + 1} 行成功`)
      this.$set(this.tableData, this.idx, this.form)
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
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
  .input_search {
    width: 50%;
  }
  .button_save {
    float: right;
    margin-left: 30px;
  }
</style>
