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
        <el-button type="primary" class="button-save" v-if="ifchange">提 交</el-button>
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
                <el-input type="textarea" v-model="props.row.sod_remarks" rows="3" :disabled="!ifchange"
                          placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="sod_iden" sortable label="物料编码" align="center"></el-table-column>
        <el-table-column prop="sod_name" sortable label="物料名称" :filters="sod_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_specification" sortable label="规格" :filters="sod_specificationSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_model" sortable label="型号" :filters="sod_modelSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_meterage" sortable label="单位" :filters="sod_meterageSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="sod_num" sortable label="请购数量" align="center">
          <template slot-scope="scope">
            <el-input
              v-if="formadd.so_type=='退换货'"
              prefix-icon="el-icon-minus"
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.sod_num"
              @input="scope.row.sod_num = inputnum(scope.row.sod_num)"
              @change="scope.row.sod_num = changenum(scope.row.sod_num)">
            </el-input>
            <el-input
              v-else
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.sod_num"
              @input="scope.row.sod_num = inputnum(scope.row.sod_num)"
              @change="scope.row.sod_num = changenum(scope.row.sod_num)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="sod_taxRate" sortable label="税率" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="13"
              :disabled="!ifchange"
              v-model="scope.row.sod_taxRate"
              @input="scope.row.sod_taxRate = inputsodTaxRate(scope.row.sod_taxRate)"
              @change="scope.row.sod_taxRate = changesodTaxRate(scope.row.sod_taxRate)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="sod_tax_unitPrice" sortable label="含税单价" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="0"
              :disabled="!ifchange"
              v-model="scope.row.sod_tax_unitPrice"
              @input="scope.row.sod_tax_unitPrice = inputsodTaxUnitPrice(scope.row.sod_tax_unitPrice)"
              @change="scope.row.sod_tax_unitPrice = changesodTaxUnitPrice(scope.row.sod_tax_unitPrice)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="sod_tax_unitPrice/(1+sod_taxRate/100)" sortable label="无税单价" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.sod_tax_unitPrice/(1+scope.row.sod_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sod_tax_unitPrice*sod_num*" sortable label="含税金额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.sod_tax_unitPrice*scope.row.sod_num).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sod_tax_unitPrice*sod_num/(1+sod_taxRate/100)" sortable label="无税金额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.sod_tax_unitPrice*scope.row.sod_num/(1+scope.row.sod_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sod_tax_unitPrice*sod_num*sod_taxRate/100/(1+sod_taxRate/100)" sortable label="税额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.sod_tax_unitPrice*scope.row.sod_num*scope.row.sod_taxRate/100/(1+scope.row.sod_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
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
    <el-dialog title="新增物料" :visible.sync="addVisible" width="90%" append-to-body>
      <Transferadd @add="addPrd" :tableHas="tableData"></Transferadd>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI} from '../../api/api'

export default {
  name: 'sell_sod',
  props: ['formadd', 'ifchange'],
  components: {
    Transferadd
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
      sod_nameSet: [],
      sod_specificationSet: [],
      sod_modelSet: [],
      sod_meterageSet: [],
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
      postAPI('/so_sod', this.formadd).then(function (res) {
        _this.tableData = res.data.list
        _this.find()
        let nameset = new Set()
        let specificationset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['sod_name'])
          specificationset.add(_this.tableData[i]['sod_specification'])
          modelset.add(_this.tableData[i]['sod_model'])
          meterageset.add(_this.tableData[i]['sod_meterage'])
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
          data.sod_iden.toLowerCase().includes(this.search.toLowerCase()) ||
          data.sod_name.toLowerCase().includes(this.search.toLowerCase()) ||
          data.sod_specification.toLowerCase().includes(this.search.toLowerCase()) ||
          data.sod_model.toLowerCase().includes(this.search.toLowerCase()) ||
          data.sod_meterage.toLowerCase().includes(this.search.toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
    },
    // 新增物料
    addPrd (val) {
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
    inputsodTaxRate (num) {
      num = num.replace(/[^\d]/g, '')
      if (num > 16) {
        num = 16
      }
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      return num
    },
    changesodTaxRate (num) {
      if (num === '') {
        num = 13
      }
      return num
    },
    inputsodTaxUnitPrice (num) {
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
    changesodTaxUnitPrice (num) {
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
