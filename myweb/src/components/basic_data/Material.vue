<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料维护
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
        <el-table-column prop="material_iden" sortable label="编码" align="center"></el-table-column>
        <el-table-column prop="material_name" sortable label="名称" :filters="material_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_specification" sortable label="规格" :filters="material_specSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_model" sortable label="型号" :filters="material_modelSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_meterage" sortable label="计量单位" :filters="material_meterageSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_attr" sortable label="存货属性" :filters="material_attrSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_creator" sortable label="创建人" :filters="material_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="material_createDate" sortable label="创建日期" align="center"></el-table-column>
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
              v-if="scope.row.material_status==='启用'"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.material_status==='停用'"
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" >
      <div class="container">
        <el-form ref="form" :model="form" label-width="100px"  class="form" >
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
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="规格" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_specification" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="型号" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.material_model" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="计量单位"  align="left">
              <el-select v-model="form.material_meterage" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in meterage_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
          <el-form-item label="存货属性"  align="left">
            <el-select v-model="form.material_attr" placeholder="请选择"  class="option" >
              <el-option key="存货" label="存货" value="存货"> </el-option>
              <el-option key="固定资产" label="固定资产" value="固定资产"> </el-option>
              <el-option key="费用" label="费用" value="费用"> </el-option>
            </el-select>
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
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="100px">
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-tag
                  :type="'success'"
                >{{editform.material_iden}}
                </el-tag>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="规格" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_specification" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="型号" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.material_model" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="计量单位"  align="left">
              <el-select v-model="editform.material_meterage" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in meterage_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="存货属性"  align="left">
              <el-select v-model="editform.material_attr" placeholder="请选择"  class="option" >
                <el-option key="存货" label="存货" value="存货"> </el-option>
                <el-option key="固定资产" label="固定资产" value="固定资产"> </el-option>
                <el-option key="费用" label="费用" value="费用"> </el-option>
              </el-select>
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
  </div>
</template>

<script>
import {postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      options: [],
      meterage_options: [],
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        material_iden: '',
        material_name: '',
        material_specification: '',
        material_model: '',
        material_meterage: '',
        material_attr: ''
      },
      material_name: '',
      material_specSet: [],
      material_nameSet: [],
      material_modelSet: [],
      material_meterageSet: [],
      material_attrSet: [],
      material_creatorSet: [],
      editform: {
        material_iden: '',
        material_name: '',
        material_specification: '',
        material_model: '',
        material_meterage: '',
        material_attr: ''
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
      this.getlist()
      this.getoptions()
      let _this = this
      postAPI('/material').then(function (res) {
        _this.tableData = res.data.list
        _this.tableDataNew = _this.tableData
        let nameset = new Set()
        let specset = new Set()
        let modelset = new Set()
        let meterageset = new Set()
        let attrset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['material_iden'])
          specset.add(_this.tableData[i]['material_specification'])
          modelset.add(_this.tableData[i]['material_model'])
          meterageset.add(_this.tableData[i]['material_meterage'])
          attrset.add(_this.tableData[i]['material_attr'])
          creatorset.add(_this.tableData[i]['material_creator'])
        }
        for (let i of nameset) {
          _this.material_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of specset) {
          _this.material_specSet.push({
            text: i,
            value: i
          })
        }
        for (let i of modelset) {
          _this.material_modelSet.push({
            text: i,
            value: i
          })
        }
        for (let i of meterageset) {
          _this.material_meterageSet.push({
            text: i,
            value: i
          })
        }
        for (let i of attrset) {
          _this.material_attrSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.material_creatorSet.push({
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
    // 新增
    handleAlter () {
      this.alterVisible = true
    },
    // 一键清除新增表单
    clearform () {
      this.form.material_attr = ''
      this.form.material_iden = ''
      this.form.material_meterage = ''
      this.form.material_model = ''
      this.form.material_specification = ''
      this.form.material_name = ''
    },
    // 禁用操作
    handleStop (row) {
      postAPI('/material', {data: row, material_status: '停用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.material_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_specification).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_model).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_meterage).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_meterage).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_attr).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.material_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      postAPI('/material', {data: row, material_status: '启用'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 获取级联选择器
    optionsAdd (parent, child, length, end) {
      if (length === end) {
        parent.push({
          value: child.type_iden,
          label: child.type_name,
          children: []
        })
        return
      }
      let pub = child.type_iden.substring(0, length)
      for (let i in parent) {
        if (parent[i].value === pub) {
          this.optionsAdd(parent[i].children, child, length + 2, end)
          return
        }
      }
      parent.push({
        value: child.type_iden,
        label: child.type_name,
        children: []
      })
    },
    getoptions () {
      let _this = this
      postAPI('/material_type').then(function (res) {
        let length = 2
        while (res.data.list.length > 0) {
          for (let i = 0; i < res.data.list.length; i++) {
            if (res.data.list[i].type_iden.length === length) {
              _this.optionsAdd(_this.options, res.data.list[i], 2, length)
              res.data.list.splice(i, 1)
              i -= 1
            }
          }
          length += 2
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 选择分类
    changeCascader (val) {
      console.log(val)
    },
    // 获取列表
    getlist () {
      let _this = this
      postAPI('/meterage').then(function (res) {
        let altermeterage = new Set()
        for (let i in res.data.list) {
          altermeterage.add(res.data.list[i]['meterage_name'])
        }
        for (let j of altermeterage) {
          _this.meterage_options.push(j)
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.material_name = row.material_name
      this.editform.material_iden = row.material_iden
      this.editform.material_specification = row.material_specification
      this.editform.material_model = row.material_model
      this.editform.material_meterage = row.material_meterage
      this.editform.material_attr = row.material_attr
      this.material_name = row.material_name
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      this.editVisible = false
      this.$message.success(`修改成功`)
      postAPI('/material', {data: this.editform, material_name: this.material_name}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      this.alterVisible = false
      this.$message.success(`新增成功`)
      this.clearform()
      postAPI('/material', {data: this.form, table: 'material'}).then(function (res) {
        console.log(res)
      }).catch(function (err) {
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
