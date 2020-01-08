<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 客户维护
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
        <el-button type="primary" icon="el-icon-plus" @click="handleAlter" class="alter-button">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.customer_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="customer_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="customer_name" sortable label="名称" :filters="customer_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="customer_type" sortable label="类型" :filters="customer_typeSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.customer_type==0?'success':''">{{scope.row.customer_type==0?'内部单位':'外部单位'}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="customer_creator" sortable label="创建人" :filters="customer_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="customer_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-unlock"
              class="red"
              @click="handleStop(scope.row)"
              v-if="scope.row.customer_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.customer_status===0"
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="70px"  class="form" >
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.customer_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.customer_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="类型"  align="left">
              <el-select v-model="form.customer_type" placeholder="请选择类型"  class="option" >
                <el-option v-for="item in customertype" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.customer_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="70px">
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.customer_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.customer_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="类型"  align="left">
              <el-select v-model="editform.customer_type" placeholder="请选择类型"  class="option" >
                <el-option v-for="item in customertype" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.customer_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      customertype: [
        {
          value: 0,
          label: '内部单位'
        },
        {
          value: 1,
          label: '外部单位'
        }
      ],
      search: '',
      form: {
        customer_iden: '',
        customer_name: '',
        customer_type: '',
        customer_remarks: '',
        customer_area: ''
      },
      customer_iden: '',
      customer_nameSet: [],
      customer_typeSet: [],
      customer_creatorSet: [],
      editform: {
        customer_iden: '',
        customer_name: '',
        customer_type: '',
        customer_remarks: '',
        customer_area: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      getAPI('/base/customers').then(function (res) {
        if (!res.data.customers) {
          return
        }
        _this.tableData = res.data.customers
        _this.pageTotal = res.data.customers.length
        _this.find()
        _this.customer_nameSet = []
        _this.customer_typeSet = []
        _this.customer_creatorSet = []
        let nameset = new Set()
        let typeset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['customer_name'])
          typeset.add(_this.tableData[i]['customer_type'])
          creatorset.add(_this.tableData[i]['customer_creator'])
        }
        for (let i of nameset) {
          _this.customer_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.customer_typeSet.push({
            text: _this.customertype[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.customer_creatorSet.push({
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
    // 一键清除新增表单
    clearform () {
      this.form.customer_iden = ''
      this.form.customer_name = ''
      this.form.customer_type = ''
      this.form.customer_remarks = ''
      this.form.customer_area = ''
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
      let _this = this
      getAPI('/base/customers').then(function (res) {
        let maxiden
        if (res.data.message) {
          maxiden = '0000001'
        } else {
          maxiden = String(parseInt(res.data.max_id) + 1)
        }
        _this.form.customer_iden = maxiden
        for (let i = 0; i < 7 - maxiden.length; i++) {
          _this.form.customer_iden = '0' + _this.form.customer_iden
        }
      })
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.customer_status = 0
          postAPI('/base/customerStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.customer_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.customer_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.customer_type).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.customer_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.customer_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.customer_status = 1
          postAPI('/base/customerStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消启用'
          })
        })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.customer_iden = row.customer_iden
      this.editform.customer_name = row.customer_name
      this.editform.customer_type = row.customer_type
      this.editform.customer_remarks = row.customer_remarks
      this.customer_iden = row.customer_iden
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      let _this = this
      if (_this.editform.customer_iden === '') {
        _this.$message.error(`编码不能为空`)
        return
      }
      if (_this.editform.customer_iden.length > 7) {
        _this.$message.error(`编码最长为7位`)
        return
      }
      if (_this.editform.customer_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      if (_this.editform.customer_type === '') {
        _this.$message.error(`请选择类型`)
        return
      }
      postAPI('/base/customerUpdate', _this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.editVisible = false
          _this.$message.success(`修改成功`)
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`修改失败`)
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      let _this = this
      if (_this.form.customer_iden === '') {
        _this.$message.error(`编码不能为空`)
        return
      }
      if (_this.form.customer_iden.length > 7) {
        _this.$message.error(`编码最长为7位`)
        return
      }
      if (_this.form.customer_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      if (_this.form.customer_type === '') {
        _this.$message.error(`请选择类型`)
        return
      }
      _this.form.customer_status = 0
      postAPI('/base/customerAdd', _this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.getData()
          _this.clearform()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`新增失败`)
        console.log(err)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    }
  }
}
</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
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
    position: relative;
  }

  .input-search {
    width: 50%;
  }
  .alter-button{
    position: absolute;
    right:0;
  }

  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: GREEN;
  }
  .inputs {
    width: 590px;
  }
</style>
