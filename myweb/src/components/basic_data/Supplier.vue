<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 供应商维护
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
                <span>{{ props.row.supply_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="supply_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="supply_name" sortable label="名称" :filters="supply_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="supply_type" sortable label="类型" :filters="supply_typeSet"
                         :filter-method="filter" align="center">
          <template slot-scope="scope">
            <el-tag :type=supplytype[scope.row.supply_type].type>{{scope.row.supply_type==0?'内部单位':'外部单位'}}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="supply_creator" sortable label="创建人" :filters="supply_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="supply_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.supply_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.supply_status===0"
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
                <el-tag :type="'success'">{{form.supply_iden}}</el-tag>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.supply_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="类型"  align="left">
              <el-select v-model="form.supply_type" placeholder="请选择类型"  class="option" >
                <el-option v-for="item in supplytype" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.supply_remarks"
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
                <el-tag :type="'success'">{{editform.supply_iden}}</el-tag>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.supply_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="类型"  align="left">
            <el-select v-model="editform.supply_type" placeholder="请选择类型"  class="option" >
              <el-option v-for="item in supplytype" v-bind:key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.supply_remarks"
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
import {postAPI, getAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      supplytype: [
        {
          value: 0,
          label: '内部单位',
          type: 'success'
        },
        {
          value: 1,
          label: '外部单位',
          type: ''
        }
      ],
      search: '',
      form: {
        supply_iden: '',
        supply_name: '',
        supply_type: '',
        supply_remarks: '',
        supply_area: ''
      },
      supply_status: '',
      supply_nameSet: [],
      supply_typeSet: [],
      supply_creatorSet: [],
      editform: {
        supply_iden: '',
        supply_name: '',
        supply_type: '',
        supply_remarks: '',
        supply_area: ''
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
      getAPI('/base/suppliers').then(function (res) {
        if (!res.data.suppliers) {
          return
        }
        _this.tableData = res.data.suppliers
        _this.pageTotal = res.data.suppliers.length
        _this.find()
        _this.supply_nameSet = []
        _this.supply_typeSet = []
        _this.supply_creatorSet = []
        let nameset = new Set()
        let typeset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['supply_name'])
          typeset.add(_this.tableData[i]['supply_type'])
          creatorset.add(_this.tableData[i]['supply_creator'])
        }
        for (let i of nameset) {
          _this.supply_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of typeset) {
          _this.supply_typeSet.push({
            text: _this.supplytype[i].label,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.supply_creatorSet.push({
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
    // 新增
    handleAlter () {
      this.alterVisible = true
      let _this = this
      getAPI('/base/suppliers').then(function (res) {
        let maxiden
        if (res.data.message) {
          maxiden = '0100001'
        } else {
          maxiden = String(parseInt(res.data.max_iden) + 1)
        }
        _this.form.supply_iden = maxiden
        for (let i = 0; i < 7 - maxiden.length; i++) {
          _this.form.supply_iden = '0' + _this.form.supply_iden
        }
      })
    },
    // 一键清除新增表单
    clearform () {
      this.form.supply_area = ''
      this.form.supply_iden = ''
      this.form.supply_name = ''
      this.form.supply_remarks = ''
      this.form.supply_type = ''
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          let data = {
            'supply_name': row.supply_name,
            'supply_iden': row.supply_iden,
            'supply_area': row.supply_area,
            'supply_type': row.supply_type,
            'supply_status': 1,
            'supply_remarks': row.supply_remarks
          }
          postAPI('/base/supplierStatus', data).then(function (res) {
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
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          let data = {
            'supply_name': row.supply_name,
            'supply_iden': row.supply_iden,
            'supply_area': row.supply_area,
            'supply_type': row.supply_type,
            'supply_status': 0,
            'supply_remarks': row.supply_remarks
          }
          postAPI('/base/supplierStatus', data).then(function (res) {
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
          String(data.supply_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.supply_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.supply_type).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.supply_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.supply_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.supply_iden = row.supply_iden
      this.editform.supply_name = row.supply_name
      this.editform.supply_type = row.supply_type
      this.editform.supply_remarks = row.supply_remarks
      this.editform.supply_status = row.supply_status
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      let _this = this
      if (_this.editform.supply_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      if (_this.editform.supply_type === '') {
        _this.$message.error(`请选择类型`)
        return
      }
      let data = {
        'supply_iden': _this.editform.supply_iden,
        'supply_name': _this.editform.supply_name,
        'supply_type': _this.editform.supply_type,
        'supply_remarks': _this.editform.supply_remarks,
        'supply_status': _this.editform.supply_status
      }
      postAPI('/base/supplierUpdate', data).then(function (res) {
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
      if (this.form.supply_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      if (_this.form.supply_type === '') {
        _this.$message.error(`请选择类型`)
        return
      }
      let data = {
        'supply_iden': _this.form.supply_iden,
        'supply_name': _this.form.supply_name,
        'supply_type': _this.form.supply_type,
        'supply_remarks': _this.form.supply_remarks,
        'supply_status': 0
      }
      postAPI('/base/supplierAdd', data).then(function (res) {
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
}</script>

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
