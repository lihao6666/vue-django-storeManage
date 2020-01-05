<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料类别维护
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
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="type_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="type_name" sortable label="名称" :filters="type_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="type_creator" sortable label="创建人" :filters="type_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="type_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.type_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.type_status===0"
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
            <el-form-item label="分类" class="inputs" align="left">
              <el-col :span="10">
                <el-cascader :options="options" :props="{ expandTrigger: 'hover', checkStrictly: true  }" clearable @change="changeCascader">
                  <template slot-scope="{ node, data }">
                    <span>{{ data.label }}</span>
                    <span v-if="!node.isLeaf"> ({{ data.children.length }}) </span>
                  </template>
                </el-cascader>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="input_iden" @input="form.type_iden = option_iden + (input_iden = inputIden(input_iden))" >
                  <template slot="prepend">{{option_iden}}</template>
                </el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.type_name" ></el-input>
              </el-col>
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
                <span>{{editform.type_iden}}</span>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.type_name" ></el-input>
              </el-col>
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
      options: [],
      option_iden: '',
      input_iden: '',
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        type_iden: '',
        type_name: '',
        type_remarks: '',
        type_area: ''
      },
      type_iden: '',
      type_nameSet: [],
      type_creatorSet: [],
      editform: {
        type_iden: '',
        type_name: '',
        type_remarks: '',
        type_area: ''
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
    // 获取级联选择器
    optionsAdd (parent, child, length, end) {
      if (length === end) {
        parent.push({
          value: child[0],
          label: child[1],
          children: []
        })
        return
      }
      let pub = child[0].substring(0, length)
      for (let i in parent) {
        if (parent[i].value === pub) {
          this.optionsAdd(parent[i].children, child, length + 2, end)
          return
        }
      }
      parent.push({
        value: child[0],
        label: child[1],
        children: []
      })
    },
    // 获取列表
    getlist () {
      let _this = this
      getAPI('/base/materialNew').then(function (res) {
        console.log(res.data)
        _this.options = []
        let length = 2
        while (res.data.material_types.length > 0) {
          for (let i = 0; i < res.data.material_types.length; i++) {
            if (res.data.material_types[i][0].length === length) {
              _this.optionsAdd(_this.options, res.data.material_types[i], 2, length)
              res.data.material_types.splice(i, 1)
              i -= 1
            }
          }
          length += 2
        }
        _this.meterage_options = res.data.meterages
      }).catch(function (err) {
        console.log(err)
      })
    },
    getData () {
      let _this = this
      getAPI('/base/materialTypes').then(function (res) {
        console.log(res.data)
        let n = res.data.max_iden.length
        let num = parseInt(res.data.max_iden) + 1
        _this.username = String(Array(n > num ? (n - ('' + num).length + 1) : 0).join(0) + num)
        _this.tableData = res.data.material_types
        _this.pageTotal = _this.tableData.length
        _this.find()
        _this.type_nameSet = []
        _this.type_creatorSet = []
        let nameset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['type_name'])
          creatorset.add(_this.tableData[i]['type_creator'])
        }
        console.log(_this.options)
        for (let i of nameset) {
          _this.type_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.type_creatorSet.push({
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
    // 选择分类
    changeCascader (val) {
      this.option_iden = val[val.length - 1]
    },
    // 编码校验
    inputIden (val) {
      if (val.length > 2) {
        val = val.substring(0, 2)
      }
      return val
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
      this.getlist()
    },
    // 一键清除新增表单
    clearform () {
      this.form.type_iden = ''
      this.form.type_iden = ''
      this.form.type_name = ''
      this.form.type_remarks = ''
      this.option_iden = ''
      this.input_iden = ''
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.type_status = 0
          postAPI('/base/materialTypeStatus', row).then(function (res) {
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
          String(data.type_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.type_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.type_status = 1
          postAPI('/base/materialTypeStatus', row).then(function (res) {
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
      this.editform.type_iden = row.type_iden
      this.editform.type_name = row.type_name
      this.editform.type_remarks = row.type_remarks
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      let _this = this
      if (_this.editform.type_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      postAPI('/base/materialTypeUpdate', this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`修改成功`)
          _this.editVisible = false
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        console.log(err)
        _this.$message.error(`修改失败`)
      })
    },
    // 保存新增
    saveAlter () {
      let _this = this
      if (!_this.form.type_iden) {
        _this.$message.error(`编码不能为空`)
        return
      }
      if (_this.input_iden.length < 2) {
        _this.$message.error(`编码必须为两位`)
        return
      }
      if (_this.form.type_name === '') {
        _this.$message.error(`名称不能为空`)
        return
      }
      _this.form.type_status = 0
      postAPI('/base/materialTypeAdd', _this.form).then(function (res) {
        console.log(res.data)
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
