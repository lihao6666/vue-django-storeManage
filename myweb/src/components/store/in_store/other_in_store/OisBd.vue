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
          v-if="ifchange"
          @click="delAllSelection"
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
        <el-button type="primary" class="button-save" v-if="ifchange" :disabled="!tableDataNew.length > 0">提 交</el-button>
        <el-button v-if="ifchange" type="primary" icon="el-icon-plus" class="button-save" @click="add">选择采购单</el-button>
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
                <el-input type="textarea" v-model="props.row.bd_remarks" rows="3" :disabled="!ifchange"
                    placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="bd_iden" sortable label="物料编码" :filters="bd_idenSet"
      :filter-method="filter"  align="center"></el-table-column>
        <el-table-column prop="bd_name" sortable label="物料名称" :filters="bd_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="bd_specification" sortable label="规格" :filters="bd_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="bd_model" sortable label="型号" :filters="bd_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="bd_meterage" sortable label="单位" :filters="bd_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="bd_paper_num" sortable label="应收数量" align="center"></el-table-column>
        <el-table-column prop="bd_real_num" sortable label="实收数量" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.bd_real_num"
              @input="scope.row.bd_real_num = inputnum(scope.row.bd_real_num)"
              @change="scope.row.bd_real_num = changenum(scope.row.bd_real_num)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="bd_unitPrice" sortable label="无税单价" align="center"></el-table-column>
        <el-table-column prop="bd_unitPrice*bd_real_num" sortable label="无税金额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.bd_unitPrice*scope.row.bd_real_num).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="bd_trans_iden" sortable label="转库单号" :filters="bd_trans_idenset"
      :filter-method="filter" align="center"></el-table-column>
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
    <el-dialog title="新增采购订单物料" :visible.sync="addVisible" width="90%" append-to-body>
      <Bdadd @add="addBd" :tableHas="tableData" :formadd="formadd" :ifhasorga="ifhasorga" :ifhasware="ifhasware"></Bdadd>
    </el-dialog>
  </div>
</template>

<script>
import { postAPI } from '../../../../api/api'
import Bdadd from './OisBdAdd.vue'

export default {
  name: 'bis_bd',
  props: ['formadd', 'ifchange'],
  components: {
    Bdadd
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
      bd_idenSet: [],
      bd_nameSet: [],
      bd_specificationSet: [],
      bd_modelSet: [],
      bd_meterageSet: [],
      bd_trans_idenset: [],
      addVisible: false,
      ifhasorga: false,
      ifhasware: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
    this.$nextTick(function () {
      if (!this.formadd.bis_orga) {
        this.addVisible = true
      }
    })
  },
  methods: {
    getData () {
      if (this.formadd.bis_iden === '') {
        return
      }
      let _this = this
      postAPI('/bis_bd', this.formadd).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let transidenset = new Set()
        let idenset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['bd_name'])
          specificationset.add(_this.tableData[i]['bd_specification'])
          modelset.add(_this.tableData[i]['bd_model'])
          meterageset.add(_this.tableData[i]['bd_meterage'])
          transidenset.add(_this.tableData[i]['bd_trans_iden'])
          idenset.add(_this.tableData[i]['bd_iden'])
        }
        for (let i of nameset) {
          _this.bd_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of idenset) {
          _this.bd_idenSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.bd_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of transidenset) {
          _this.bd_trans_idenset.push({
            text: i,
            value: i
          })
        }
        for (let i of specificationset) {
          _this.bd_specificationSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.bd_modelSet.push({
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
        data.bd_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.bd_name.toLowerCase().includes(this.search.toLowerCase()) ||
        data.bd_specification.toLowerCase().includes(this.search.toLowerCase()) ||
        data.bd_trans_iden.toLowerCase().includes(this.search.toLowerCase()) ||
        data.bd_model.toLowerCase().includes(this.search.toLowerCase()) ||
        data.bd_meterage.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      if (this.formadd.bis_orga === '' || this.formadd.bis_warehouse === '') {
        this.ifhasorga = false
      } else {
        this.ifhasorga = true
      }
      if (this.formadd.bis_warehouse === '') {
        this.ifhasware = false
      } else {
        this.ifhasware = true
      }
    },
    // 新增物料通过转库单
    addBd (val) {
      for (let i in val) {
        val[i].bd_real_num = val[i].bd_paper_num
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
      if (num === '') {
        num = 1
      }
      return num
    },
    inputodTaxRate (num) {
      num = num.replace(/[^\d]/g, '')
      if (num > 16) {
        num = 16
      }
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      return num
    },
    changeodTaxRate (num) {
      if (num === '') {
        num = 13
      }
      return num
    },
    inputodTaxUnitPrice (num) {
      if (num !== '' && num.substr(0, 1) === '.') {
        num = ''
      }
      num = num.replace(/^0*(0\.|[1-9])/, '$1') // 粘贴不生效
      num = num.replace(/[^\d.]/g, '') // 清除“数字”和“.”以外的字符
      num = num.replace(/\.{2,}/g, '.') // 只保留第一个. 清除多余的
      num = num.replace('.', '$#$').replace(/\./g, '').replace('$#$', '.')
      num = num.replace(/^()*(\d+)\.(\d\d).*$/, '$1$2.$3')// 只能输入两个小数
      if (num.indexOf('.') < 0 && num !== '') { // 以上已经过滤，此处控制的是如果没有小数点，首位不能为类似于 01、02的金额
        if (num.substr(0, 1) === '0' && num.length === 2) {
          num = num.substr(1, num.length)
        }
      }
      return num
    },
    changeodTaxUnitPrice (num) {
      if (num === '') {
        num = 0
      }
      num = Number(num).toFixed(2)
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
