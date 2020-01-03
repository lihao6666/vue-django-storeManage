<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 付款协议
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
        <el-button type="primary" icon="el-icon-plus" class="button-save" @click="add" v-if="ifchange">新增</el-button>
      </div>
      <el-table
        :data="tableData"
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
                <el-input type="textarea" v-model="props.row.pay_remarks" rows="3" :disabled="!ifchange"
                    placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable></el-input>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="pay_batch" sortable label="付款批次" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="1"
              class="little"
              :disabled="!ifchange"
              v-model="scope.row.pay_batch"
              @input="scope.row.pay_batch = inputPayPrepay(scope.row.pay_batch)"
              @change="scope.row.pay_batch = changePayPrepay(scope.row.pay_batch)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="pay_rate" sortable label="付款比例" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="1"
              class="little"
              :disabled="!ifchange"
              v-model="scope.row.pay_rate"
              @input="scope.row.pay_rate = inputPayRate(scope.row.pay_rate)"
              @change="scope.row.pay_rate = changePayRate(scope.row.pay_rate)">
            </el-input>
            <span>%</span>
          </template>
        </el-table-column>
        <el-table-column prop="pay_price" sortable label="付款金额" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="0"
              class="little"
              :disabled="!ifchange"
              v-model="scope.row.pay_price"
              @input="scope.row.pay_price = inputPayPrice(scope.row.pay_price)"
              @change="scope.row.pay_price = changePayPrice(scope.row.pay_price)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="pay_planDate" sortable label="计划付款日期" align="center">
          <template slot-scope="scope">
            <el-date-picker
              v-model="scope.row.pay_planDate"
              class="big"
              type="date"
              :disabled="!ifchange"
              placeholder="选择日期">
            </el-date-picker>
          </template>
        </el-table-column>
        <el-table-column prop="pay_prepay" sortable label="是否预付款" align="center">
          <template slot-scope="scope">
            <el-select v-model="scope.row.pay_prepay" placeholder="请选择" class="little" :disabled="!ifchange">
              <el-option key="1" label="是" value="1"></el-option>
              <el-option key="0" label="否" value="0"></el-option>
            </el-select>
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
  </div>
</template>

<script>
import {postAPI} from '../../../api/api'

export default {
  name: 'pc_pay',
  props: ['formadd', 'ifchange'],
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      tableData: [],
      multipleSelection: [],
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    changeSelect (val) {
      console.log(val)
    },
    getData () {
      if (this.formadd.pc_iden === '') {
        return
      }
      let _this = this
      postAPI('/base/pc_pay', this.formadd).then(function (res) {
        _this.tableData = res.data.list
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
    filterHandler (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    // 新增
    add () {
      this.tableData.push({})
    },
    // 修改
    inputPayPrepay (num) {
      num = num.replace(/[^\d]/g, '')
      if (num > 10) {
        num = 10
      }
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      return num
    },
    changePayPrepay (num) {
      if (num === '') {
        num = 1
      }
      return num
    },
    inputPayRate (num) {
      num = num.replace(/[^\d]/g, '')
      if (num > 100) {
        num = 100
      }
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      return num
    },
    changePayRate (num) {
      if (num === '') {
        num = 1
      }
      return num
    },
    inputPayPrice (num) {
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
    changePayPrice (num) {
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
  .button-save {
    float: right;
    margin-left: 30px;
  }
  .little {
    width: 60%;
  }
  .big {
    width: 90%;
  }
</style>
